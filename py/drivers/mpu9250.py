# https://github.com/micropython-IMU/micropython-mpu9x50/blob/master/mpu9250.py

from drivers.imu import MPU6050, bytes_toint, MPUException
from drivers.vector3d import Vector3d


class MPU9250(MPU6050):
    _mag_addr = 12
    _chip_id = 113

    def __init__(self, side_str, device_addr=None, transposition=(0, 1, 2), scaling=(1, 1, 1)):

        super().__init__(side_str, device_addr, transposition, scaling)
        self._mag = Vector3d(transposition, scaling, self._mag_callback)
        self.accel_filter_range = 0
        self.gyro_filter_range = 0
        self._mag_stale_count = 0
        self.mag_correction = self._magsetup()
        self._mag_callback()

    @property
    def sensors(self):
        return self._accel, self._gyro, self._mag


    @property
    def temperature(self):
        try:
            self._read(self.buf2, 0x41, self.mpu_addr)
        except OSError:
            raise MPUException(self._I2Cerror)
        return bytes_toint(self.buf2[0], self.buf2[1])/333.87 + 21


    @property
    def gyro_filter_range(self):
        try:
            self._read(self.buf1, 0x1A, self.mpu_addr)
            res = self.buf1[0] & 7
        except OSError:
            raise MPUException(self._I2Cerror)
        return res

    @gyro_filter_range.setter
    def gyro_filter_range(self, filt):
        if filt in range(8):
            try:
                self._write(filt, 0x1A, self.mpu_addr)
            except OSError:
                raise MPUException(self._I2Cerror)
        else:
            raise ValueError('Filter coefficient must be between 0 and 7')

    @property
    def accel_filter_range(self):
        try:
            self._read(self.buf1, 0x1D, self.mpu_addr)
            res = self.buf1[0] & 7
        except OSError:
            raise MPUException(self._I2Cerror)
        return res

    @accel_filter_range.setter
    def accel_filter_range(self, filt):
        if filt in range(8):
            try:
                self._write(filt, 0x1D, self.mpu_addr)
            except OSError:
                raise MPUException(self._I2Cerror)
        else:
            raise ValueError('Filter coefficient must be between 0 and 7')

    def _magsetup(self):
        try:
            self._write(0x0F, 0x0A, self._mag_addr)
            self._read(self.buf3, 0x10, self._mag_addr)
            self._write(0, 0x0A, self._mag_addr)
            self._write(0x16, 0x0A, self._mag_addr)
        except OSError:
            raise MPUException(self._I2Cerror)
        mag_x = (0.5*(self.buf3[0] - 128))/128 + 1
        mag_y = (0.5*(self.buf3[1] - 128))/128 + 1
        mag_z = (0.5*(self.buf3[2] - 128))/128 + 1
        return (mag_x, mag_y, mag_z)

    @property
    def mag(self):
        return self._mag

    def _mag_callback(self):
        try:
            self._read(self.buf1, 0x02, self._mag_addr)
            if self.buf1[0] & 1 == 0:
                return self._mag
            self._read(self.buf6, 0x03, self._mag_addr)
            self._read(self.buf1, 0x09, self._mag_addr)
        except OSError:
            raise MPUException(self._I2Cerror)
        if self.buf1[0] & 0x08 > 0:
            self._mag_stale_count += 1
            return
        self._mag._ivector[1] = bytes_toint(self.buf6[1], self.buf6[0])
        self._mag._ivector[0] = bytes_toint(self.buf6[3], self.buf6[2])
        self._mag._ivector[2] = -bytes_toint(self.buf6[5], self.buf6[4])
        scale = 0.15
        self._mag._vector[0] = self._mag._ivector[0]*self.mag_correction[0]*scale
        self._mag._vector[1] = self._mag._ivector[1]*self.mag_correction[1]*scale
        self._mag._vector[2] = self._mag._ivector[2]*self.mag_correction[2]*scale
        self._mag_stale_count = 0

    @property
    def mag_stale_count(self):
        return self._mag_stale_count

    def get_mag_irq(self):
        self._read(self.buf1, 0x02, self._mag_addr)
        if self.buf1[0] == 1:
            self._read(self.buf6, 0x03, self._mag_addr)
            self._read(self.buf1, 0x09, self._mag_addr)
            self._mag._ivector[1] = 0
            if self.buf1[0] & 0x08 == 0:
                self._mag._ivector[1] = bytes_toint(self.buf6[1], self.buf6[0])
                self._mag._ivector[0] = bytes_toint(self.buf6[3], self.buf6[2])
                self._mag._ivector[2] = -bytes_toint(self.buf6[5], self.buf6[4])
