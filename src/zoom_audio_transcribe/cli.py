from __future__ import print_function, unicode_literals

import os
from os.path import expanduser
from typing import Dict, List

from art import tprint
from PyInquirer import Separator, prompt

from smarttranscribe_audio_transcribe.convert import _convert_from_m4a_to_wav
from smarttranscribe_audio_transcribe.transcribe import transcribe

smarttranscribe_DIR = os.path.join(expanduser("~"), "Documents", "smarttranscribe")


def _get_smarttranscribe_list_recordings_list() -> List[str]:
    """Get the list of all the recordings."""
    # The local path for smarttranscribe recording is ~/Documents/smarttranscribe
    # Get the home directory
    file_list = os.listdir(smarttranscribe_DIR)
    files = []
    for f in file_list:
        files.append(f)
        files.append(Separator())
    return files


def user_response() -> Dict[str, str]:
    questions = [
        {
            "type": "list",
            "name": "smarttranscribe_recording",
            "choices": _get_smarttranscribe_list_recordings_list(),
            "message": "Which smarttranscribe recording do you want to convert?",
        }
    ]

    answers = prompt(questions)
    return answers


def main() -> None:
    """Main."""
    tprint("smarttranscribe Audio Transcribe")
    user_res = user_response()
    folder_name = user_res["smarttranscribe_recording"]

    _convert_from_m4a_to_wav(os.path.join(smarttranscribe_DIR, folder_name))

    transcribed_text = transcribe(
        os.path.join(os.path.join(smarttranscribe_DIR, folder_name, "{}.wav").format(folder_name))
    )

    with open(
        os.path.join(smarttranscribe_DIR, folder_name, "{}.txt".format(folder_name)), "w"
    ) as f:
        f.write(transcribed_text)


if __name__ == "__main__":
    main()
