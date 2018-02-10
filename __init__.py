# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.


# Visit https://docs.mycroft.ai/skill.creation for more detailed information
# on the structure of this skill and its containing folder, as well as
# instructions for designing your own skill based on this template.


# Import statements: the list of outside modules you'll be using in your
# skills, whether from other files in mycroft-core or from external libraries
from os import listdir
from os.path import dirname, isfile, join
from random import randrange

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util import play_mp3


__author__ = 'kathyreid'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)

# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class MalibuStacySkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(MalibuStacySkill, self).__init__(name="MalibuStacySkill")
        self.process = None
        self.theFiles = []

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        self.load_data_files(dirname(__file__))

        what_would_malibu_stacy_do_intent = IntentBuilder("WhatWouldMalibuStacyDoIntent").\
            require("WhatWouldMalibuStacyDoKeyword").build()
        self.register_intent(what_would_malibu_stacy_do_intent, self.handle_what_would_malibu_stacy_do_intent)

        malibu_stacy_intent = IntentBuilder("MalibuStacyIntent").\
            require("MalibuStacyKeyword").build()
        self.register_intent(malibu_stacy_intent, self.handle_what_would_malibu_stacy_do_intent)

    # The "handle_xxxx_intent" functions define Mycroft's behavior when
    # each of the skill's intents is triggered: in this case, he simply
    # speaks a response. Note that the "speak_dialog" method doesn't
    # actually speak the text it's passed--instead, that text is the filename
    # of a file in the dialog folder, and Mycroft speaks its contents when
    # the method is called.
    def handle_what_would_malibu_stacy_do_intent(self, message):

        self.load_data_files(dirname(__file__))

        # Create an array of the .mp3 files in the mp3 directory
        for name in listdir(join(dirname(__file__), "mp3")):
            self.theFiles.append(name)

        # Randomly select one of the array of mp3 files to play and play it
        index = randrange(0, len(self.theFiles))
        self.process = play_mp3(join(dirname(__file__), "mp3", self.theFiles[index]))

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution.
    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return MalibuStacySkill()
