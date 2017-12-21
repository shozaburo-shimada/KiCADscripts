#!/usr/bin/env python
#
# kicadPcb2switchSciencePcb.py
#
# Author:   Hiromasa Ihara (miettal)
# Created:  2015-12-02
#
# Updated: Shozaburo Shimada, 2017 for Fusion PCB
#

import os
import shutil
import zipfile

from pcbnew import *

layers = {
  "GTL":F_Cu,
  "GBL":B_Cu,
  "GTO":F_SilkS,
  "GBO":B_SilkS,
  "GTS":F_Mask,
  "GBS":B_Mask,
  "GML":Edge_Cuts,
}

def convert() :
  board = GetBoard()
  plot_controller = PLOT_CONTROLLER(board)
  plot_options = plot_controller.GetPlotOptions()
  excellon_writer = EXCELLON_WRITER(board)

  board_basename = os.path.basename(board.GetFileName()).split('.')[0]
  pcb_dirname = "{}_switchsience_pcb".format(board_basename)
  print "board_basename:", board_basename
  print "pcb_dirname:", pcb_dirname

  #GERBER OUTPUT
  # Options
  plot_options.SetOutputDirectory(pcb_dirname)
  plot_options.SetFormat(PLOT_FORMAT_GERBER)

  plot_options.SetPlotFrameRef(False)             #Plot sheet reference on all layers
  plot_options.SetPlotPadsOnSilkLayer(False)      #Plot pads on silkscreen
  plot_options.SetPlotValue(False)                #Plot footprint values
  plot_options.SetPlotReference(True)             #Plot footprint references
  plot_options.SetPlotInvisibleText(False)        #Force plotting of invisible values/references
  plot_options.SetPlotViaOnMaskLayer(True)        #Do not tent vias
  plot_options.SetExcludeEdgeLayer(True)          #Exclude PCB edge layer form other layers
  plot_options.SetUseAuxOrigin(True)              #Use auxiliary axis as origin

  plot_options.SetLineWidth(FromMM(0.1))          #Default line width

  plot_options.SetUseGerberProtelExtensions(True) #Use Protel file extensions
  plot_options.SetUseGerberAttributes(False)      #Include extended attributes
  plot_options.SetSubtractMaskFromSilk(False)     #Subtract soldermask from silkscreen

  plot_options.SetGerberPrecision(6)              #Resolution of coordinates in Gerber files (6: 4.6 (unit mm))

  # Export, Rename
  for (ext, sym) in layers.items() :
    plot_controller.SetLayer(sym)
    plot_controller.OpenPlotfile(ext, PLOT_FORMAT_GERBER, "")
    plot_controller.PlotLayer()

    pcb_dirpath = plot_controller.GetPlotDirName()
    gerber_raw_filepath = plot_controller.GetPlotFileName()
    gerber_filepath = os.path.join(pcb_dirpath, "{}.{}".format(board_basename, ext))
    print "gerber_filepath:", gerber_filepath

    plot_controller.ClosePlot()
    shutil.move(gerber_raw_filepath, gerber_filepath)

  #DRILL OUTPUT
  # Options

  excellon_writer.SetFormat(True, EXCELLON_WRITER.SUPPRESS_LEADING, 3, 3)
  excellon_writer.SetOptions(False, False, wxPoint(0, 0), False)
  excellon_writer.CreateDrillandMapFilesSet(pcb_dirpath, True, False)
  # Export, Rename
  drill_raw_filepath = os.path.join(pcb_dirpath, "{}.drl".format(board_basename))
  drill_filepath = os.path.join(pcb_dirpath, "{}.TXT".format(board_basename))
  print "drill_filepath:", drill_filepath
  shutil.move(drill_raw_filepath, drill_filepath)

  #Build ZIP
  pcb_zipfilepath = "{}.zip".format(pcb_dirpath[:-1])
  print "pcb_zipfilepath:", pcb_zipfilepath
  with zipfile.ZipFile(pcb_zipfilepath, 'w') as zip_f :
    #GERBER
    for (ext, sym) in layers.items() :
      gerber_filepath = os.path.join(pcb_dirpath, "{}.{}".format(board_basename, ext))
      gerber_filename = os.path.join(pcb_dirname, "{}.{}".format(board_basename, ext))
      zip_f.write(gerber_filepath, gerber_filename)

    #DRILL
    drill_filepath = os.path.join(pcb_dirpath, "{}.TXT".format(board_basename))
    drill_filename = os.path.join(pcb_dirname, "{}.TXT".format(board_basename))
    zip_f.write(drill_filepath, drill_filename)

  print "success"

convert()
