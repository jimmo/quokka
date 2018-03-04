class Series():
    def __init__(self, x_or_y=[], y=None,
                 name=None,
                 x_units=None, x_label=None,
                 y_units=None, y_label=None,
                 min_x=None, max_x=None,
                 min_y=None, max_y=None,
                 marker=None, val_format=None):
        # Store data, detect if we have x&y, or just y series data
        if y is None:
            self.x = None
            self.y = x_or_y
            self.ndim = 1
        else:
            self.x = x_or_y
            self.y = y
            self.ndim = 2
            if len(self.x) != len(self.y):
                raise ValueError("x and y arrays must be of the same length")

        # Store series metadata
        self.name = name
        self.x_units = x_units
        self.x_label = x_label
        self.y_units = y_units
        self.y_label = y_label

        # Store display limits
        if self.ndim == 2:
            self.upd_min_x = min_x is None
            self.upd_max_x = max_x is None
            if self.x:
                self.min_x = min_x if not self.upd_min_x else min(self.x)
                self.max_x = max_x if not self.upd_max_x else max(self.x)
            else:
                self.min_x = float("-inf")
                self.max_x = float("inf")
        self.upd_min_y = min_y is None
        self.upd_max_y = max_y is None
        if self.y:
            self.min_y = min_y if not self.upd_min_y else min(self.y)
            self.max_y = max_y if not self.upd_max_y else max(self.y)
        else:
            self.min_y = float("-inf")
            self.max_y = float("inf")

        # Store marker
        self.marker = marker
        if marker is None:
            marker = "p"

        # Store value formatter
        self.val_format = val_format

    def __repr__(self):
        if self.ndim == 2:
            return "{}({}, {}, ...)".format(self.__class__.__name__, self.x, self.y)
        else:
            return "{}({}, ...)".format(self.__class__.__name__, self.y)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, index):
        if self.ndim == 2:
            return (self.x[index], self.y[index])
        return self.y[index]

    def __iter__(self):
        if self.ndim == 2:
            return zip(self.x, self.y)
        return iter(self.y)

    def _upd_x_lim(self, val):
        if self.upd_min_x and val < self.min_x:
            self.min_x = val
        if self.upd_max_x and val > self.max_x:
            self.max_x = val

    def _upd_y_lim(self, val):
        if self.upd_min_y and val < self.min_y:
            self.min_y = val
        if self.upd_max_y and val > self.max_y:
            self.max_y = val

    def push(self, x_or_val, val=None):
        if self.ndim == 2:
            if val is None:
                raise ValueError("Both x and val must be given for 2-dimensional array")
            self.x.push(x_or_val)
            self.y.push(val)
            self._upd_x_lim(x_or_val)
            self._upd_y_lim(val)
        else:
            if val is not None:
                raise ValueError("Only 1 value should be given for for a 1-dimensional array")
            self.y.push(x_or_val)
            self._upd_y_lim(x_or_val)

class BoundedSeries(Series):
    def __init__(self, max_len, x_or_y=[], y=None, *args, **kwargs):
        # Check max_len is given and valid
        if not isinstance(max_len, int) or max_len <= 0:
            raise ValueError("max_len must be an integer greater than 0")
        self.max_len = max_len

        # Initialize other attributes
        super().__init__(x_or_y, y, *args, **kwargs)

        # Turn x and y into length limited arrays
        x = self.x
        y = self.y
        if self.ndim == 2:
            self.x = [0]*max_len
            for i, pt in enumerate(x[-max_len:]):
                self.x[i] = pt
            self._upd_x_lim(None)
        self.y = [0]*max_len
        for i, pt in enumerate(y[-max_len:]):
            self.y[i] = pt
        self._upd_y_lim(None)

        # And keep track of the filled length, and the next index to fill
        self.len = min(self.max_len, len(x_or_y))
        self.next_slot = self.len % self.max_len

    def __repr__(self):
        if self.ndim == 1:
            y_str = list(self)
            return "{}({}, ...)".format(self.__class__.__name__, y_str)
        else:
            x_str = []
            y_str = []
            for x, y in self:
                x_str.append(x)
                y_str.append(y)
            return "{}({}, {})".format(self.__class__.__name__, x_str, y_str)

    def __len__(self):
        return self.len

    def __iter__(self):
        def circ_iter(start, length):
            start = start % length
            if self.ndim == 1:
                yield self.y[start]
            else:
                yield (self.x[start], self.y[start])

            ind = (start + 1) % length
            while ind != start:
                if self.ndim == 2:
                    yield (self.x[ind], self.y[ind])
                else:
                    yield self.y[ind]
                ind = (ind + 1) % length
        return circ_iter(self.next_slot, self.len)

    def _upd_x_lim(self, val):
        if self.upd_min_x:
            self.min_x = min(self.x)
        if self.upd_max_x:
            self.max_x = max(self.x)

    def _upd_y_lim(self, val):
        if self.upd_min_y:
            self.min_y = min(self.y)
        if self.upd_max_y:
            self.max_y = max(self.y)

    def push(self, x_or_val, val=None):
        if self.ndim == 2:
            if val is None:
                raise ValueError("Both x and y must be given for a 2-dimensional array")
            self.x[self.next_slot] = x_or_val
            self.y[self.next_slot] = val
            self._upd_x_lim(x_or_val)
            self._upd_y_lim(val)
        else:
            if val is not None:
                raise ValueError("Only one parameter may be given for a 1-dimensional array")
            self.y[self.next_slot] = x_or_val
            self._upd_y_lim(x_or_val)
        self.next_slot = (self.next_slot + 1) % self.max_len
        self.len = max(self.next_slot, self.len)
