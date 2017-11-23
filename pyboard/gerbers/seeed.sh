#!/bin/bash
mkdir -p /tmp/quokka
rm /tmp/quokka/*

cp quokka-F.Cu.gbr /tmp/quokka/quokka.GTL
cp quokka-B.Cu.gbr /tmp/quokka/quokka.GBL

cp quokka-In1.Cu.gbr /tmp/quokka/quokka.GL2
cp quokka-In2.Cu.gbr /tmp/quokka/quokka.GL3

cp quokka-F.Mask.gbr /tmp/quokka/quokka.GTS
cp quokka-B.Mask.gbr /tmp/quokka/quokka.GBS

cp quokka-F.SilkS.gbr /tmp/quokka/quokka.GTO
cp quokka-B.SilkS.gbr /tmp/quokka/quokka.GBO

cp quokka-Edge.Cuts.gbr /tmp/quokka/quokka.GML

cp quokka.drl /tmp/quokka/quokka.DRL
cp quokka-NPTH.drl /tmp/quokka/quokka-NPTH.DRL

pushd /tmp/quokka
zip quokka.zip quokka.G* quokka.DRL
popd

mv /tmp/quokka/quokka.zip .
