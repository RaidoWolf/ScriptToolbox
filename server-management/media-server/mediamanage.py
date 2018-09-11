#!/usr/bin/env python

import argparse
import configparser
import os
import sys
from shutil import which
from subprocess import call

LIBRARY_ROOT = os.getcwd()
ORIGINAL_ROOT = os.path.join(LIBRARY_ROOT, "original")

CONFIG = configparser.ConfigParser()

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

OPUS_TARGET_BITRATE = 128 # in kilobits per second
VORBIS_QUALITY = 6 # 0-10 (it's VBR)
LAME_BASELINE_BITRATE = 128 # in kilobits per second
AAC_BITRATE = 128000 # in bits per second

DO_ENCODE_OPUS = False
DO_ENCODE_VORBIS = False
DO_ENCODE_MP3 = False
DO_ENCODE_AAC = False

DO_GENERATE_CONFIG = False

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
        self.path = path
        self.rel = os.path.relpath(path, ORIGINAL_ROOT)

    def mirrorOpus (self, force=False):
        outPath = changeFileExtension(os.path.join(LIBRARY_ROOT, "opus", self.rel), ".ogg")
        outDir = os.path.dirname(outPath)
        if not force:
            if os.path.exists(outPath):
                return True
        ensurePath(outDir)
        verbose("encoding opus >>", self.rel)
        call(["ffmpeg", "-i", self.path, "-acodec", "libopus", "-vn", "-b:a", str(OPUS_TARGET_BITRATE)+"k", "-vbr", "on", "-compression_level", "10", outPath])
        return False

    def mirrorVorbis (self, force=False):
        outPath = changeFileExtension(os.path.join(LIBRARY_ROOT, "vorbis", self.rel), ".ogg")
        outDir = os.path.dirname(outPath)
        if not force:
            if os.path.exists(outPath):
                return True
        ensurePath(outDir)
        verbose("encoding vorbis >>", self.rel)
        call(["ffmpeg", "-i", self.path, "-c:a", "libvorbis", "-vn", "-q:a", str(VORBIS_QUALITY), outPath])
        return False

    def mirrorMp3 (self, force=False):
        outPath = changeFileExtension(os.path.join(LIBRARY_ROOT, "mp3", self.rel), ".mp3")
        outDir = os.path.dirname(outPath)
        if not force:
            if os.path.exists(outPath):
                return True
        ensurePath(outDir)
        vebose("encoding mp3 >>", self.rel)
        call(["lame", "-h", "-v", "-V", "2", "-b", str(LAME_BASELINE_BITRATE), self.path, outPath])
        return False

    def mirrorAac (self, force=False):
        outPath = changeFileExtension(os.path.join(LIBRARY_ROOT, "aac", self.rel), ".m4a")
        outDir = os.path.dirname(outPath)
        if not force:
            if os.path.exists(outPath):
                return True
        ensurePath(outDir)
        verbose("encoding aac >>", self.rel)
        call(["fdkaac", "--profile", "2", "--bitrate-mode", "0", "--bitrate", str(AAC_BITRATE), "-o", outPath, self.path])
        return False

def generateMirrors (audioFiles, opus, vorbis, mp3, aac):
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
        if opus:   file.mirrorOpus()
        if vorbis: file.mirrorVorbis()
        if mp3:    file.mirrorMp3()
        if aac:    file.mirrorAac()
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

def writeConfigFile (config):
    with open(os.path.join(LIBRARY_ROOT, "mediamanage.ini"), "w") as file:
        config["Opus"] = {
            "enabled": DO_ENCODE_OPUS,
            "target_bitrate": OPUS_TARGET_BITRATE}
        config["Vorbis"] = {
            "enabled": DO_ENCODE_VORBIS,
            "quality": VORBIS_QUALITY}
        config["MP3"] = {
            "enabled": DO_ENCODE_MP3,
            "baseline_bitrate": LAME_BASELINE_BITRATE}
        config["AAC"] = {
            "enabled": DO_ENCODE_AAC,
            "bitrate": AAC_BITRATE / 1000}
        config.write(file)

def parseArgs ():
    global DO_ENCODE_OPUS
    global DO_ENCODE_VORBIS
    global DO_ENCODE_MP3
    global DO_ENCODE_AAC
    global DO_GENERATE_CONFIG
    global OPUS_TARGET_BITRATE
    global VORBIS_QUALITY
    global LAME_BASELINE_BITRATE
    global AAC_BITRATE
    ap = argparse.ArgumentParser(description="Manage a media library.")
    ap.add_argument("--encode-opus",   dest="opus",  action="store_true", default=False,
        help="Enable re-encoding library using Opus codec (original is not modified).")
    ap.add_argument("--encode-vorbis", dest="vorbis", action="store_true", default=False,
        help="Enable re-encoding library using Vorbis codec (original is not modified).")
    ap.add_argument("--encode-mp3",    dest="mp3",   action="store_true", default=False,
        help="Enable re-encoding library using MP3 codec (original is not modified).")
    ap.add_argument("--encode-aac",    dest="aac",   action="store_true", default=False,
        help="Enable re-encoding library using AAC codec (original is not modified).")
    ap.add_argument("--generate-config", dest="config", action="store_true", default=False,
        help="Generate a mediamanage.ini config file in the current directory, incorporating all command line options.")
    ap.add_argument("--opus-target-bitrate", dest="opus_bitrate", action="store", type=int, default=128,
        help="Set the target bitrate (VBR) for the Opus encoder. (kbps)")
    ap.add_argument("--vorbis-quality", dest="vorbis_quality", action="store", type=float, default=6.5,
        help="Set the quality (VBR) for the Vorbis encoder. (0-10)")
    ap.add_argument("--mp3-baseline-bitrate", dest="mp3_bitrate", action="store", type=int, default=128,
        help="Set the baseline bitrate (VBR) for the MP3 encoder. (kbps)")
    ap.add_argument("--aac-bitrate", dest="aac_bitrate", action="store", type=int, default=128,
        help="Set the bitrate (CBR) for the AAC encoder. (kbps)")
    args = ap.parse_args()
    DO_ENCODE_OPUS = True if args.opus else False
    DO_ENCODE_VORBIS = True if args.vorbis else False
    DO_ENCODE_MP3 = True if args.mp3 else False
    DO_ENCODE_AAC = True if args.aac else False
    DO_GENERATE_CONFIG = True if args.config else False
    OPUS_TARGET_BITRATE = args.opus_bitrate
    VORBIS_QUALITY = args.vorbis_quality
    LAME_BASLINE_BITRATE = args.mp3_bitrate
    AAC_BITRATE = args.aac_bitrate * 1000

configFile = findFileAbove("mediamanage.ini", LIBRARY_ROOT)
if configFile != None:
    with open(configFile, "r") as file:
        CONFIG.read_file(file)
        if CONFIG.has_section("Opus"):
            if CONFIG.has_option("Opus", "enabled"):
                if CONFIG["Opus"]["enabled"]:
                    DO_ENCODE_OPUS = True
            if CONFIG.has_option("Opus", "target_bitrate"):
                if isinstance(CONFIG["Opus"]["target_bitrate"], int):
                    OPUS_TARGET_BITRATE = CONFIG["Opus"]["target_bitrate"]
        if CONFIG.has_section("Vorbis"):
            if CONFIG.has_option("Vorbis", "enabled"):
                if CONFIG["Vorbis"]["enabled"]:
                    DO_ENCODE_VORBIS = True
            if CONFIG.has_option("Vorbis", "quality"):
                if isinstance(CONFIG["Vorbis"]["quality"], float):
                    VORBIS_QUALITY = CONFIG["Vorbis"]["quality"]
        if CONFIG.has_section("MP3"):
            if CONFIG.has_option("MP3", "enabled"):
                if CONFIG["MP3"]["enabled"]:
                    DO_ENCODE_MP3 = True
            if CONFIG.has_option("MP3", "baseline_bitrate"):
                if isinstance(CONFIG["MP3"]["baseline_bitrate"], int):
                    LAME_BASELINE_BITRATE = CONFIG["MP3"]["baseline_bitrate"]
        if CONFIG.has_section("AAC"):
            if CONFIG.has_option("AAC", "enabled"):
                if CONFIG["AAC"]["enabled"]:
                    DO_ENCODE_AAC = True
            if CONFIG.has_option("AAC", "bitrate"):
                if isinstance(CONFIG["AAC"]["bitrate"], int):
                    AAC_BITRATE = CONFIG["AAC"]["bitrate"] * 1000

parseArgs()

if DO_ENCODE_OPUS:
    requireFfmpeg()
if DO_ENCODE_VORBIS:
    requireFfmpeg()
if DO_ENCODE_MP3:
    requireLame()
if DO_ENCODE_AAC:
    requireFdk()

if DO_GENERATE_CONFIG:
    writeConfigFile(CONFIG)

for root, dirnames, filenames in os.walk(ORIGINAL_ROOT):
    for filename in filenames:
        if filename.lower().endswith(AUDIO_FILE_EXTENSIONS):
            ORIGINAL_FILES.append(AudioFile(os.path.join(root, filename)))

generateMirrors(ORIGINAL_FILES,
    DO_ENCODE_OPUS,
    DO_ENCODE_VORBIS,
    DO_ENCODE_MP3,
    DO_ENCODE_AAC)
