# -*- coding: utf-8 -*-

#実行方法
#pcbnewのツール->スクリプトコンソールから
#>>> execfile('C:\Users\Shozaburo\Documents\kicad\script\script2.py')

import pcbnew
import re
import math

(
    HORIZON_THEN_VERTICAL,
    VERTICAL_THEN_HORIZON
) = range(0,2)

#MODULEのオブジェクトmoduleを受け取り、
#moduleのリファレンスから数字部分だけを抽出して数値として返す
def __extractRefNumber(module):
    matchResult = re.findall('\d+', module.GetReference())
    return int(matchResult[0])

#正規表現にマッチしたMODULEをリストにして返す
#sort=Trueにするとリファレンスの番号順にソートする
def findModulesByRe(pattern, sort=False):
    re_pattern = re.compile(pattern)
    moduleList = []
    for module in pcbnew.GetBoard().GetModules():
        if re_pattern.match( module.GetReference() ):
            moduleList.append(module)
    if sort:
        moduleList = sorted(moduleList, key=__extractRefNumber)

    return moduleList

#部品を格子上に並べる
#start:始点座標(x,y)
#space:間隔(x,y)
#priority:moduleListの要素を縦と横どちらを優先して並べていくか
#    HORIZON_THEN_VERTICAL か VERTICAL_THEN_HORIZON
#size:priorityで指定した先に並べる方向に何個並べるか
def arrangeInMatrix(moduleList, start, space, size, priority = HORIZON_THEN_VERTICAL):
    i,j = 0,0
    for index, module in enumerate(moduleList):
        if priority == HORIZON_THEN_VERTICAL:
            j = int( index%size )
            i = int( index/size )
        elif priority == VERTICAL_THEN_HORIZON:
            j = int( index/size )
            i = int( index%size )
        posx = start[0] + j*space[0]
        posy = start[1] + i*space[1]
        module.SetPosition(pcbnew.wxPointMM(posx,posy))

#部品の向きをまとめて変更する(度)
def rotate(moduleList, orientation):
    for module in moduleList:
        module.SetOrientation( int(orientation*10) )

#pcbnewで開いている基板(BORAD)への参照を取得する
#board = pcbnew.GetBoard()

#ダイオードへの参照を全検索してリストにいれる
ledList = findModulesByRe("D\d+", True)

#Layerをそろえる
for module in ledList:
    if module.IsFlipped():
        pass
    else:
        module.Flip(module.GetPosition())

#Referenceの一括表示非表示
def visibleref(moduleList, visibility):
    for module in moduleList:
        module.Reference().SetVisible(visibility)

#配置する
arrangeInMatrix(ledList, (115.25, 106.25), (2.5, 2.5), 9, VERTICAL_THEN_HORIZON)

#角度を揃える
rotate(ledList, 45)

#Refの一括非表示
visibleref(ledList, False)
