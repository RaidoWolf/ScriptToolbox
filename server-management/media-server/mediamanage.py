#!/usr/bin/env python3

import argparse
import configparser
import os
import re
import sys
from mutagen import File
from shutil import copy2, which
from subprocess import call

LIBRARY_ROOT = os.getcwd()
ORIGINAL_ROOT = os.path.join(LIBRARY_ROOT, "original")

AUDIO_FILE_EXTENSIONS = (
    ".flac",
    ".alac",
    ".ogg",
    ".mp3",
    ".m4a",
    ".aac",
    ".wma",
    ".wav")

ORIGINAL_FILES = []

FORCE_REENCODE = False

OPUS_TARGET_BITRATE = 160 # in kilobits per second
VORBIS_QUALITY = 6 # 0-10 (it's VBR)
LAME_BASELINE_BITRATE = 128 # in kilobits per second
AAC_BITRATE = 128000 # in bits per second

DO_ENCODE_OPUS = False
DO_ENCODE_VORBIS = False
DO_ENCODE_MP3 = False
DO_ENCODE_AAC = False

DO_GENERATE_CONFIG = False

DO_PASSTHROUGH_COVER = False
DO_COPY_EXT_COVERS = False
DO_EMBED_EXT_COVER = False
DO_EXTRACT_COVER = False

def verbose (*msg):
    print(*msg, file=sys.stdout)

def notice (*msg):
    print(*msg, file=sys.stdout)

def warning (*msg):
    print("WARNING: ", *msg, file=sys.stderr)

def error (*msg):
    print("ERROR:", *msg, file=sys.stderr)

def changeFileExtension (filename, newExtension):
    return os.path.splitext(filename)[0]+newExtension

def ensurePath (path):
    if not os.path.exists(path):
        os.makedirs(path)
    return True

def isSubpath (path, directory):
    path = os.path.realpath(path)
    directory = os.path.realpath(directory)
    relative = os.path.relpath(path, directory)
    return not relative.startswith(os.pardir + os.sep)

def findFileAbove (filename, directory):
    path = os.path.realpath(
        os.path.join(
            os.path.abspath(directory), filename))
    while (True):
        if os.path.isfile(path):
            return path
        if (path == "/"):
            path = None
            break
        path = os.path.dirname(path)
    return None

def commandExists (command):
    if (which(command) == None):
        return False
    return True

class AudioFile:
    def __init__ (self, path):
        self.mut = File(path);
        self.path = path
        self.rel = os.path.relpath(path, ORIGINAL_ROOT)

    _regexPreferredCover = re.compile('^cover\.(jpe?g|png)$', re.IGNORECASE)
    _regexSecondaryCover = re.compile('^cover\.(jpe?g|png)$')

    def getDirectory ():
        return os.path.dirname(self.path)

    def hasEmbeddedCover ():
        try:
            pics = self.mut.pictures
            if pics:
                return True
        except Exception:
            pass
        if 'covr' in self.mut or 'APIC:' in self.mut:
            return True
        return False

    def hasExternalCover ():
        for file in os.listdir(self.getDirectory()):
            if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg') or file.lower().endswith('.png'):
                return True
        return False

    def getExternalCoverPath ():
        cover = False
        priority = -1
        for file in os.listdir(self.getDirectory()):
            if re.match(_regexPreferredCover, os.path.filename(file)):
                return file
            if re.match(_regexSecondaryCover, os.path.filename(file)):
                if priority <= 1:
                    if cover == False:
                        cover = file
                        priority = 1
                    elif file < cover:
                        cover = file
                        priority = 1
            if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg') or file.lower().endswith('.png'):
                if priority <= 0:
                    if cover == False:
                        cover = file
                        priority = 0
                    elif file < cover:
                        cover = file
                        priority = 0
        return cover

    def mirrorOpus (self, passCover=False, embedCover=False, force=False):
        outPath = changeFileExtension(os.path.join(LIBRARY_ROOT, "opus", self.rel), ".ogg")
        outDir = os.path.dirname(outPath)
        if not force:
            if os.path.exists(outPath):
                return True
        ensurePath(outDir)
        verbose("encoding opus >>", self.rel)
        if passCover:
            call(["ffmpeg", "-i", self.path, "-acodec", "libopus", "-b:a", str(OPUS_TARGET_BITRATE)+"k", "-vbr", "on", "-compression_level", "10", outPath])
        else:
            call(["ffmpeg", "-i", self.path, "-acodec", "libopus", "-vn", "-b:a", str(OPUS_TARGET_BITRATE)+"k", "-vbr", "on", "-compression_level", "10", outPath])
        return False

    def mirrorVorbis (self, passCover=False, embedCover=False, force=False):
        outPath = changeFileExtension(os.path.join(LIBRARY_ROOT, "vorbis", self.rel), ".ogg")
        outDir = os.path.dirname(outPath)
        if not force:
            if os.path.exists(outPath):
                return True
        ensurePath(outDir)
        verbose("encoding vorbis >>", self.rel)
        if passCover:
            call(["ffmpeg", "-i", self.path, "-c:a", "libvorbis", "-q:a", str(VORBIS_QUALITY), outPath])
        else:
            call(["ffmpeg", "-i", self.path, "-c:a", "libvorbis", "-vn", "-q:a", str(VORBIS_QUALITY), outPath])
        return False

    def mirrorMp3 (self, passCover=False, embedCover=False, force=False):
        outPath = changeFileExtension(os.path.join(LIBRARY_ROOT, "mp3", self.rel), ".mp3")
        outDir = os.path.dirname(outPath)
        if not force:
            if os.path.exists(outPath):
                return True
        ensurePath(outDir)
        verbose("encoding mp3 >>", self.rel)
        call(["lame", "-h", "-v", "-V", "2", "-b", str(LAME_BASELINE_BITRATE), self.path, outPath])
        return False

    def mirrorAac (self, passCover=False, embedCover=False, force=False):
        outPath = changeFileExtension(os.path.join(LIBRARY_ROOT, "aac", self.rel), ".m4a")
        outDir = os.path.dirname(outPath)
        if not force:
            if os.path.exists(outPath):
                return True
        ensurePath(outDir)
        verbose("encoding aac >>", self.rel)
        call(["fdkaac", "--profile", "2", "--bitrate-mode", "0", "--bitrate", str(AAC_BITRATE), "-o", outPath, self.path])
        return False

def generateMirrors (audioFiles, opus, vorbis, mp3, aac, passCover=False, embedCover=False, force=False):
    if not isinstance(audioFiles, list):
        warning("generateMirrors list of audioFiles was not a list - mirrors will not be generated")
        return False
    opusRoot =   os.path.join(LIBRARY_ROOT, "opus")
    vorbisRoot = os.path.join(LIBRARY_ROOT, "vorbis")
    mp3Root =    os.path.join(LIBRARY_ROOT, "mp3")
    aacRoot =    os.path.join(LIBRARY_ROOT, "aac")
    if opus:   ensurePath(opusRoot)
    if vorbis: ensurePath(vorbisRoot)
    if mp3:    ensurePath(mp3Root)
    if aac:    ensurePath(aacRoot)
    for file in audioFiles:
        if not isinstance(file, AudioFile):
            warning("generateMirrors encountered an element of audioFile that is not an instance of AudioFile - skipping")
            continue
        if opus:   file.mirrorOpus(passCover, embedCover, force)
        if vorbis: file.mirrorVorbis(passCover, embedCover, force)
        if mp3:    file.mirrorMp3(passCover, embedCover, force)
        if aac:    file.mirrorAac(passCover, embedCover, force)
    return True

def requireLame ():
    if not commandExists("lame"):
        error("lame command must be installed")
        sys.exit(1)
        return False
    return True

def requireFdk ():
    if not commandExists("fdkaac"):
        error("fdkaac command must be installed")
        sys.exit(1)
        return False
    return True

def requireFfmpeg ():
    if not commandExists("ffmpeg"):
        error("ffmpeg command must be installed")
        sys.exit(1)
        return False
    return True

def writeConfigFile ():
    with open(os.path.join(LIBRARY_ROOT, "mediamanage.ini"), "w") as file:
        config = configparser.ConfigParser();
        config["Process"] = {
            "force_reencode": FORCE_REENCODE }
        config["Opus"] = {
            "enabled": DO_ENCODE_OPUS,
            "target_bitrate": OPUS_TARGET_BITRATE }
        config["Vorbis"] = {
            "enabled": DO_ENCODE_VORBIS,
            "quality": VORBIS_QUALITY }
        config["MP3"] = {
            "enabled": DO_ENCODE_MP3,
            "baseline_bitrate": LAME_BASELINE_BITRATE }
        config["AAC"] = {
            "enabled": DO_ENCODE_AAC,
            "bitrate": AAC_BITRATE / 1000 }
        config["Cover"] = {
            "passthrough": DO_PASSTHROUGH_COVER,
            "embed": DO_EMBED_EXT_COVER,
            "extract": DO_EXTRACT_COVER }
        config.write(file)

def parseConfig ():
    global FORCE_REENCODE
    global DO_ENCODE_OPUS
    global DO_ENCODE_VORBIS
    global DO_ENCODE_MP3
    global DO_ENCODE_AAC
    global DO_GENERATE_CONFIG
    global OPUS_TARGET_BITRATE
    global VORBIS_QUALITY
    global LAME_BASELINE_BITRATE
    global AAC_BITRATE
    global DO_PASSTHROUGH_COVER
    global DO_COPY_EXT_COVERS
    global DO_EMBED_EXT_COVER
    global DO_EXTRACT_COVER
    config = configparser.ConfigParser()
    configFile = findFileAbove("mediamanage.ini", LIBRARY_ROOT)
    if configFile != None:
        with open(configFile, "r") as file:
            config.read_file(file)
            if config.has_section("Process"):
                if config.has_option("Process", "force_reencode"):
                    FORCE_REENCODE = True if config["Process"]["force_reencode"] else False
            if config.has_section("Opus"):
                if config.has_option("Opus", "enabled"):
                    DO_ENCODE_OPUS = True if config["Opus"]["enabled"] == "True" else False
                if config.has_option("Opus", "target_bitrate"):
                    if isinstance(config["Opus"]["target_bitrate"], int):
                        OPUS_TARGET_BITRATE = config["Opus"]["target_bitrate"]
            if config.has_section("Vorbis"):
                if config.has_option("Vorbis", "enabled"):
                    DO_ENCODE_VORBIS = True if config["Vorbis"]["enabled"] == "True" else False
                if config.has_option("Vorbis", "quality"):
                    if isinstance(config["Vorbis"]["quality"], float):
                        VORBIS_QUALITY = config["Vorbis"]["quality"]
            if config.has_section("MP3"):
                if config.has_option("MP3", "enabled"):
                    DO_ENCODE_MP3 = True if config["MP3"]["enabled"] == "True" else False
                if config.has_option("MP3", "baseline_bitrate"):
                    if isinstance(config["MP3"]["baseline_bitrate"], int):
                        LAME_BASELINE_BITRATE = config["MP3"]["baseline_bitrate"]
            if config.has_section("AAC"):
                if config.has_option("AAC", "enabled"):
                    DO_ENCODE_AAC = True if config["AAC"]["enabled"] == "True" else False
                if config.has_option("AAC", "bitrate"):
                    if isinstance(config["AAC"]["bitrate"], int):
                        AAC_BITRATE = config["AAC"]["bitrate"] * 1000
            if config.has_section("Cover"):
                if config.has_option("Cover", "passthrough"):
                    DO_PASSTHROUGH_COVER = True if config["Cover"]["passthrough"] == "True" else False
                if config.has_option("Cover", "copy"):
                    DO_COPY_EXT_COVERS = True if config["Cover"]["copy"] == "True" else False
                if config.has_option("Cover", "embed"):
                    DO_EMBED_EXT_COVER = True if config["Cover"]["embed"] == "True" else False
                if config.has_option("Cover", "extract"):
                    DO_EXTRACT_COVER = True if config["Cover"]["extract"] == "True" else False

def parseArgs ():
    global FORCE_REENCODE
    global DO_ENCODE_OPUS
    global DO_ENCODE_VORBIS
    global DO_ENCODE_MP3
    global DO_ENCODE_AAC
    global DO_GENERATE_CONFIG
    global OPUS_TARGET_BITRATE
    global VORBIS_QUALITY
    global LAME_BASELINE_BITRATE
    global AAC_BITRATE
    global DO_PASSTHROUGH_COVER
    global DO_COPY_EXT_COVERS
    global DO_EMBED_EXT_COVER
    global DO_EXTRACT_COVER
    ap = argparse.ArgumentParser(description="Manage a media library.")
    ap.add_argument("--force",         dest="force",  action="store_true",
        help="Force reencoding of all generated files (original is not modified)")
    ap.add_argument("--encode-opus",   dest="opus",   action="store_true",
        help="Enable re-encoding library using Opus codec (original is not modified).")
    ap.add_argument("--encode-vorbis", dest="vorbis", action="store_true",
        help="Enable re-encoding library using Vorbis codec (original is not modified).")
    ap.add_argument("--encode-mp3",    dest="mp3",    action="store_true",
        help="Enable re-encoding library using MP3 codec (original is not modified).")
    ap.add_argument("--encode-aac",    dest="aac",    action="store_true",
        help="Enable re-encoding library using AAC codec (original is not modified).")
    ap.add_argument("--generate-config", dest="config", action="store_true",
        help="Generate a mediamanage.ini config file in the current directory, incorporating all command line options.")
    ap.add_argument("--opus-target-bitrate", dest="opus_bitrate", action="store", type=int,
        help="Set the target bitrate (VBR) for the Opus encoder. (kbps)")
    ap.add_argument("--vorbis-quality", dest="vorbis_quality", action="store", type=float,
        help="Set the quality (VBR) for the Vorbis encoder. (0-10)")
    ap.add_argument("--mp3-baseline-bitrate", dest="mp3_bitrate", action="store", type=int,
        help="Set the baseline bitrate (VBR) for the MP3 encoder. (kbps)")
    ap.add_argument("--aac-bitrate",   dest="aac_bitrate", action="store", type=int,
        help="Set the bitrate (CBR) for the AAC encoder. (kbps)")
    ap.add_argument("--enable-cover-passthrough", dest="cover_passthrough", action="store_true",
        help="Enable cover image passthrough (copying it from the original file's metadata to the new one).")
    ap.add_argument("--enable-cover-copy", dest="cover_copy", action="store_true",
        help="Enable cover image copying (copying external files to the generated folder).")
    ap.add_argument("--enable-cover-embed", dest="cover_embed", action="store_true",
        help="Enable cover image embedding (copying from external images to the file metadata).")
    ap.add_argument("--enable-cover-extract", dest="cover_extract", action="store_true",
        help="Enable cover image extracting (copying from file metadata to an actual image file).")
    args, leftover = ap.parse_known_args()
    if args.force is not False:
        FORCE_REENCODE =        True
    if args.opus is not False:
        DO_ENCODE_OPUS =        True
    if args.vorbis is not False:
        DO_ENCODE_VORBIS =      True
    if args.mp3 is not False:
        DO_ENCODE_MP3 =         True
    if args.aac is not False:
        DO_ENCODE_AAC =         True
    if args.config is not False:
        DO_GENERATE_CONFIG =    True
    if args.opus_bitrate is not None:
        OPUS_TARGET_BITRATE =   args.opus_bitrate
    if args.vorbis_quality is not None:
        VORBIS_QUALITY =        args.vorbis_quality
    if args.mp3_bitrate is not None:
        LAME_BASLINE_BITRATE =  args.mp3_bitrate
    if args.aac_bitrate is not None:
        AAC_BITRATE =           args.aac_bitrate * 1000
    if args.cover_passthrough is not False:
        DO_PASSTHROUGH_COVER =  True
    if args.cover_copy is not False:
        DO_COPY_EXT_COVERS =    True
    if args.cover_embed is not False:
        DO_EMBED_EXT_COVER =    True
    if args.cover_extract is not False:
        DO_EXTRACT_COVER =      True

parseConfig()
parseArgs()

if DO_GENERATE_CONFIG:
    writeConfigFile()
if DO_ENCODE_OPUS:
    requireFfmpeg()
if DO_ENCODE_VORBIS:
    requireFfmpeg()
if DO_ENCODE_MP3:
    requireLame()
if DO_ENCODE_AAC:
    requireFdk()

if not DO_ENCODE_OPUS and not DO_ENCODE_VORBIS and not DO_ENCODE_MP3 and not DO_ENCODE_AAC:
    sys.exit(0)

for root, dirnames, filenames in os.walk(ORIGINAL_ROOT):
    for filename in filenames:
        if filename.lower().endswith(AUDIO_FILE_EXTENSIONS):
            ORIGINAL_FILES.append(AudioFile(os.path.join(root, filename)))

generateMirrors(ORIGINAL_FILES,
    DO_ENCODE_OPUS,
    DO_ENCODE_VORBIS,
    DO_ENCODE_MP3,
    DO_ENCODE_AAC,
    DO_PASSTHROUGH_COVER,
    DO_EMBED_EXT_COVER)

if DO_COPY_EXT_COVERS:
    for root, dirnames, filenames in os.walk(ORIGINAL_ROOT):
        for filename in filenames:
            if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg') or filename.lower().endswith('.png'):
                path = os.path.join(root, filename)
                rel = os.path.relpath(path, ORIGINAL_ROOT)
                if DO_ENCODE_OPUS:
                    verbose("copying cover image to opus >> ", rel)
                    copy2(path, os.path.join(LIBRARY_ROOT, 'opus', rel))
                if DO_ENCODE_VORBIS:
                    verbose("copying cover image to vorbis >> ", rel)
                    copy2(path, os.path.join(LIBRARY_ROOT, 'vorbis', rel))
                if DO_ENCODE_MP3:
                    verbose("copying cover image to mp3 >> ", rel)
                    copy2(path, os.path.join(LIBRARY_ROOT, 'mp3', rel))
                if DO_ENCODE_AAC:
                    verbose("copying cover image to aac >> ", rel)
                    copy2(path, os.path.join(LIBRARY_ROOT, 'aac', rel))
