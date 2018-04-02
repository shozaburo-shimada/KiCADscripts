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
import datetime

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

metalmasks = {
  "GTP":F_Paste,
  "GBP":B_Paste,
}

def convert() :
  board = GetBoard()
  plot_controller = PLOT_CONTROLLER(board)
  plot_options = plot_controller.GetPlotOptions()
  excellon_writer = EXCELLON_WRITER(board)

  board_basename = os.path.basename(board.GetFileName()).split('.')[0]
  gerber_dirname = "gerber"
  pcbvendor = "fusionPCB"

  #GERBER OUTPUT
  # Options
  plot_options.SetOutputDirectory(gerber_dirname)
  plot_options.SetFormat(PLOT_FORMAT_GERBER)

  plot_options.SetPlotFrameRef(False)             #Plot sheet reference on all layers
  plot_options.SetPlotPadsOnSilkLayer(False)      #Plot pads on silkscreen
  plot_options.SetPlotValue(False)                #Plot footprint values
  plot_options.SetPlotReference(True)             #Plot footprint references
  plot_options.SetPlotInvisibleText(False)        #Force plotting of invisible values/references
  plot_options.SetPlotViaOnMaskLayer(True)        #False:w/ resist, True: Do not tent vias(w/o resist)
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
    print "pcb_dirpath:", pcb_dirpath
    gerber_raw_filepath = plot_controller.GetPlotFileName()
    print "gerber_raw_filepath:", gerber_raw_filepath
    gerber_filepath = os.path.join(pcb_dirpath, "{}.{}".format(board_basename, ext))
    print "gerber_filepath:", gerber_filepath

    plot_controller.ClosePlot()
    shutil.move(gerber_raw_filepath, gerber_filepath)

  # Metal Mask Export
  for (ext, sym) in metalmasks.items() :
     plot_controller.SetLayer(sym)
     plot_controller.OpenPlotfile(ext, PLOT_FORMAT_GERBER, "")
     plot_controller.PlotLayer()

     pcb_dirpath = plot_controller.GetPlotDirName()
     gerber_raw_filepath = plot_controller.GetPlotFileName()
     print "gerber_raw_filepath:", gerber_raw_filepath
     gerber_filepath = os.path.join(pcb_dirpath, "{}.{}".format(board_basename, ext))
     print "gerber_filepath:", gerber_filepath

     plot_controller.ClosePlot()
     shutil.move(gerber_raw_filepath, gerber_filepath)

  #DRILL OUTPUT
  # Options
  d_units = True # True: Millimeters, False: inches
  d_zerosformats = EXCELLON_WRITER.SUPPRESS_LEADING
  d_mirror = False
  d_minheader = True
  d_origin = board.GetAuxOrigin()
  d_merge_th = True

  excellon_writer.SetFormat(d_units, d_zerosformats, 3, 3)
  excellon_writer.SetOptions(d_mirror, d_minheader, d_origin, d_merge_th)
  excellon_writer.CreateDrillandMapFilesSet(pcb_dirpath, True, False)

  # Export, Rename
  drill_raw_filepath = os.path.join(pcb_dirpath, "{}.drl".format(board_basename))
  drill_filepath = os.path.join(pcb_dirpath, "{}.TXT".format(board_basename))
  print "drill_filepath:", drill_filepath
  shutil.copyfile(drill_raw_filepath, drill_filepath)

  #Build ZIP
  todaydetail = datetime.datetime.today()
  #pcb_zipfilepath = "{}_{}.zip".format(pcb_dirpath[:-1],todaydetail.strftime("_%Y%m%d%H%M"))
  pcb_zipfilename = "{}_{}_{}.zip".format(board_basename, pcbvendor, todaydetail.strftime("%Y%m%d%H%M"))
  pcb_zipfilepath = "{}{}".format(pcb_dirpath, pcb_zipfilename)
  print "pcb_zipfilepath:", pcb_zipfilepath

  with zipfile.ZipFile(pcb_zipfilepath, 'w') as zip_f :
    #GERBER
    for (ext, sym) in layers.items() :
      gerber_filepath = os.path.join(pcb_dirpath, "{}.{}".format(board_basename, ext))
      gerber_filename = "{}.{}".format(board_basename, ext)
      zip_f.write(gerber_filepath, gerber_filename)

    #DRILL
    drill_filepath = os.path.join(pcb_dirpath, "{}.TXT".format(board_basename))
    drill_filename = "{}.TXT".format(board_basename)
    zip_f.write(drill_filepath, drill_filename)

  print "success"

convert()
