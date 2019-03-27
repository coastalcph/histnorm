#!/usr/bin/env bash

printUsage () {
    echo "Usage: convert_to_orignorm.sh TRAIN [TEST [DEV]] --to DIRECTORY" >&2
}

printHelp () {
    printUsage
    echo "" >&2
    echo "Prepares parallel two-colum text files for use with cSMTiser/Moses." >&2
    echo "" >&2
    echo "Options:" >&2
    echo "  -h, --help         Show this helpful text." >&2
    echo "  --to DIRECTORY     Output directory for writing the processed files." >&2
}

declare -a PARAMS

while (( "$#" )); do
  case "$1" in
    --to)
      TODIR="$2"
      shift 2
      ;;
    -h|--help)
      printHelp
      exit 0
      ;;
    --) # end argument parsing
      shift
      break
      ;;
    -*|--*=) # unsupported flags
      printUsage
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS+=("$1")
      shift
      ;;
  esac
done

if [[ ( ${#PARAMS[@]} -lt 1 ) || ( ${#PARAMS[@]} -gt 3 ) ]] ; then
    printUsage
    exit 1
fi

if [ -z "$TODIR" ] ; then
    printUsage
    exit 1
fi

cut -f1 "${PARAMS[0]}" > "$TODIR/train.orig"
cut -f2 "${PARAMS[0]}" > "$TODIR/train.norm"
if [[ ${#PARAMS[@]} -gt 1 ]] ; then
    cut -f1 "${PARAMS[1]}" > "$TODIR/test.orig"
    cut -f2 "${PARAMS[1]}" > "$TODIR/test.norm"
fi
if [[ ${#PARAMS[@]} -gt 2 ]] ; then
    cut -f1 "${PARAMS[2]}" > "$TODIR/dev.orig"
    cut -f2 "${PARAMS[2]}" > "$TODIR/dev.norm"
fi
