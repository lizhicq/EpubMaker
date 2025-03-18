tell application "nPlayer"
	open "/Users/lizhicq/GitHub/EpubMaker/data/audio/神级大魔头/001-第1章 炎黄星.wav"
end tell

tell application "System Events"
	activate application "nPlayer" -- Ensure nPlayer is active
	
	tell process "nPlayer"
		
		get menu bar 1
		get menu "Playback" of menu bar 1
		get menu item "Playback Rate" of menu "Playback" of menu bar 1
		
		perform action "AXShowMenu" of menu item "Playback Rate" of menu "Playback" of menu bar 1
		
		get menu of menu item "Playback Rate" of menu "Playback" of menu bar 1
		get menu item 1 of menu of menu item "Playback Rate" of menu "Playback" of menu bar 1
		
		click menu item 1 of menu of menu item "Playback Rate" of menu "Playback" of menu bar 1
		click menu item 1 of menu of menu item "Playback Rate" of menu "Playback" of menu bar 1
		click menu item 1 of menu of menu item "Playback Rate" of menu "Playback" of menu bar 1
		click menu item 1 of menu of menu item "Playback Rate" of menu "Playback" of menu bar 1
		click menu item 1 of menu of menu item "Playback Rate" of menu "Playback" of menu bar 1
		click menu item 1 of menu of menu item "Playback Rate" of menu "Playback" of menu bar 1
		click menu item 1 of menu of menu item "Playback Rate" of menu "Playback" of menu bar 1
		click menu item 1 of menu of menu item "Playback Rate" of menu "Playback" of menu bar 1
		click menu item 1 of menu of menu item "Playback Rate" of menu "Playback" of menu bar 1
		click menu item 1 of menu of menu item "Playback Rate" of menu "Playback" of menu bar 1
		
	end tell
end tell