#!/bin/bash
arg1=$1
if [ "$arg1" != "" ]; then
	if [ "$arg1" == "--help" ] || [ "$arg1" == "-h" ]; then
		echo "bash smosh_vlc.sh [url-of-embed-link]"
		echo "or bash smosh_vlc.sh and type embed link when prompted."
		echo "To get the embed link, click on a video on the Smosh website, then click the share link in the top-right corner. Copy the text in the 'src' tag."
	else
		content=$(curl $arg1)
	fi
else
	echo "embed link from Smosh website?"
	read link
	content=$(curl $link)
fi
output=$(echo "$content" | grep -o "http.*2240.*mp4")
if [ "$output" != "" ]; then
	echo "Parsed result (720p MP4):"
	echo $output
	echo "Open with VLC? (y/n)"
	read open
	if [ "$open" == "y" ]; then
		echo "CTRL^C to exit VLC log."
		vlc $output & disown
		exit
	elif [ "$open" == "n" ]; then
		echo "Exiting."
		exit
	else
		echo "Invalid option (must be 'y' or 'n'). Exiting."
		exit
	fi
else
	echo "No results found."
fi
exit
