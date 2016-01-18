#!/bin/bash
for dir in `ls "$PWD"`; do
    if [ -d "$dir" ]; then
        archive="$dir"
        archive+=".tar.xz"
        if [ -e "$archive" ]; then
            echo "Deleting old archive: $archive"
            rm -rf "$archive"
        fi
        if [ "$?" != "0" ]; then
            echo "Error: failed to delete old archive file at $archive."
            exit 1
        fi
        echo "Creating archive of $dir at $archive"
        tar -Jcvf "$archive" "$dir"
        if [ "$?" != "0" ]; then
            echo "Error: failed to create archive $archive of directory $dir."
            exit 1
        fi
    fi
    echo "Complete!"
done

exit 0
