#include <FileConstants.au3>
#include <MsgBoxConstants.au3>
#include <GUIConstantsEx.au3>
#include <Excel.au3>
#include <IE.au3>

Dim $txtFilepath = ''
Dim $hGui = GUICreate('Open URL from Excel', 400, 200)
Dim $hInput = GUICtrlCreateInput('Enter a path', 10, 10, 150)
Dim $fileButton = GUICtrlCreateButton('Choose File', 180, 10, 70)
Dim $stRow=GUICtrlCreateInput('Enter start row', 10, 40, 150)
Dim $endRow=GUICtrlCreateInput('Enter end row', 180, 40, 150)
Dim $hButton = GUICtrlCreateButton('Ok', 10, 70, 50)

GUISetState(@SW_SHOW, $hGui)

While 1
	Switch GUIGetMsg()
		Case $GUI_EVENT_CLOSE
			ExitLoop
		 Case $fileButton
			;chooseFile()
			;ControlSetText("Setting Text","",$hInput,chooseFile())
			GUICtrlSetData($hInput,chooseFile())
			;MsgBox($MB_SYSTEMMODAL, "", "You chose the following file:" & @CRLF & chooseFile())
		Case $hButton
			GUISetState(@SW_HIDE, $hGui)
			If FileExists(GUICtrlRead($hInput)) Then
				$txtFilepath = GUICtrlRead($hInput)
				;chooseFile()
				;MsgBox(0, 'Valid Input', $txtFilepath)
				ExcelRecords(GUICtrlRead($hInput),GUICtrlRead($stRow),GUICtrlRead($endRow))
				GUIDelete($hGui)
				ExitLoop
			Else
				MsgBox(0, 'Input Error', 'Invalid Input, try again.')
				GUISetState(@SW_SHOW, $hGui)
			EndIf
	EndSwitch
WEnd

Func chooseFile()
Local Const $sMessage = "Select a single file of any type."

    ; Display an open dialog to select a file.
    Local $sFileOpenDialog = FileOpenDialog($sMessage, @WindowsDir & "\", "All (*.*)", $FD_FILEMUSTEXIST)
    If @error Then
        ; Display the error message.
        MsgBox($MB_SYSTEMMODAL, "", "No file was selected.")

        ; Change the working directory (@WorkingDir) back to the location of the script directory as FileOpenDialog sets it to the last accessed folder.
        FileChangeDir(@ScriptDir)
    Else
        ; Change the working directory (@WorkingDir) back to the location of the script directory as FileOpenDialog sets it to the last accessed folder.
        FileChangeDir(@ScriptDir)

        ; Replace instances of "|" with @CRLF in the string returned by FileOpenDialog.
        $sFileOpenDialog = StringReplace($sFileOpenDialog, "|", @CRLF)
		;ControlSetText("Setting Text","",$hInput,$sFileOpenDialog)
		;$hInput=$sFileOpenDialog
        ; Display the selected file.
        ;MsgBox($MB_SYSTEMMODAL, "", "You chose the following file:" & @CRLF & $sFileOpenDialog)

	 EndIf
	 Return $sFileOpenDialog
  EndFunc

Func ExcelRecords($filepathVar,$startrow,$endrow)
; Create application object and open an example workbook

Local $oExcel = _Excel_Open()
If @error <> 0 Then Exit MsgBox($MB_SYSTEMMODAL, "Excel UDF: _Excel_BookAttach Example", "Error creating the Excel application object." & @CRLF & "@error = " & @error & ", @extended = " & @extended)
Local $oWorkbook = _Excel_BookOpen($oExcel, $filepathVar,True,False)
$sSheet="Sheet1"
;MsgBox("","Header",$filepathVar)
Local $aData = _Excel_RangeRead($oWorkbook, $sSheet, "A"&$startrow&":A"&$endrow, 1, True)
;MsgBox("","Headder","A"&$startrow&":A"&$endrow)
_ArrayDisplay($aData)
For $iRow = 0 To $endrow-$startrow
      ;  ConsoleWrite("Row " & $iRow + 1 & " is 1 and value of column B is " & $aData[$iRow][0])
	;	$oIE = _IEAttach("", "instance", 1)
	;	 If IsObj($oIE) Then
	  ; Open new tab
	;	 $oIE.Navigate2($aData[$iRow][0], $navOpenInNewTab)
	;	 Else
	  ; Launch browser
	;	 $oIE = _IECreate($aData[$iRow][0])
	;	 EndIf
	ShellExecute('chrome.exe', $aData[$iRow][0])
Next

If @error Then
    MsgBox($MB_SYSTEMMODAL, "Excel UDF: _Excel_BookAttach Example", "Error opening workbook '" & $filepathVar & @CRLF & "@error = " & @error & ", @extended = " & @extended)
    _Excel_Close($oExcel)
    Exit
EndIf

; Attach to the first Workbook where the file name matches
;Local $sWorkbook = $filepathVar
;$oWorkbook = _Excel_BookAttach($sWorkbook, "filename")
;$sSheet="Sheet1"
;MsgBox("","Header",$filepathVar)
;Local $aData = _Excel_RangeRead($oWorkbook, $sSheet, "A1:A6", 1, True)
;_ArrayDisplay($aData)


;If @error Then Exit MsgBox($MB_SYSTEMMODAL, "Excel UDF: _Excel_BookAttach Example 2", "Error attaching to '" & $sWorkbook & "'." & @CRLF & "@error = " & @error & ", @extended = " & @extended)
;MsgBox($MB_SYSTEMMODAL, "Excel UDF: _Excel_BookAttach Example 2", "Search by 'filename':" & @CRLF & @CRLF & "Successfully attached to Workbook '" & $sWorkbook & "'." & @CRLF & @CRLF & "Value of cell A2: " & $oWorkbook.Activesheet.Range("A2").Value)
EndFunc