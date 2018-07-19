# encoding: UTF-8
#
# PhotoFilmStrip - Creates movies out of your pictures.
#
# Copyright (C) 2011 Jens Goepfert
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import logging
import os

from photofilmstrip.action.IAction import IAction

from photofilmstrip.lib.Settings import Settings
from photofilmstrip.lib.util import CheckFile
from photofilmstrip.core.Renderer import RENDERERS
from photofilmstrip.core.RenderEngine import RenderEngineSlideshow, \
    RenderEngineTimelapse
from photofilmstrip.core.RenderJob import RenderJob
from photofilmstrip.core.GPlayer import GPlayer


class ActionRender(IAction):

    def __init__(self, photoFilmStrip,
                 profile,
                 rendererClass, draftMode,
                 outpath=None):
        self.__photoFilmStrip = photoFilmStrip
        self.__profile = profile
        self.__rendererClass = rendererClass
        self.__draftMode = draftMode
        self.__outpath = outpath

        self.__renderJob = None

    def GetName(self):
        return _(u'Start')

    def _CheckAndGetOutFile(self):
        if self.__outpath == "-":
            return

        projFile = self.__photoFilmStrip.GetFilename()
        baseDir = os.path.dirname(projFile)
        baseDir = os.path.join(baseDir, self.__profile.GetName())
        if not os.path.isdir(baseDir):
            os.makedirs(baseDir)

        outFile = os.path.join(baseDir,
                               os.path.basename(os.path.splitext(projFile)[0]))
        return outFile

    def _SaveSettings(self):
        settings = Settings()
        settings.SetLastProfile(self.__profile.GetName())

        try:
            idxRenderer = RENDERERS.index(self.__rendererClass)
        except ValueError:
            return

        settings.SetUsedRenderer(idxRenderer)

    def Execute(self):
        audioFiles = []
        audioLength = 0
        for audioFile in self.__photoFilmStrip.GetAudioFiles():
            if CheckFile(audioFile):
                length = GPlayer(audioFile).GetLength()
                audioFiles.append(audioFile)
                logging.debug("Using audiofile '%s' with length: %s", audioFile, length)
                audioLength += length
            else:
                logging.warning("Missing audiofile '%s'!", audioFile)

        outFile = self._CheckAndGetOutFile()

        self._SaveSettings()

        savedProps = Settings().GetRenderProperties(self.__rendererClass.__name__)
        for prop in self.__rendererClass.GetProperties():
            value = savedProps.get(prop.lower(), self.__rendererClass.GetProperty(prop))
            self.__rendererClass.SetProperty(prop, value)

        totalLength = self.__photoFilmStrip.GetDuration(False)
        if totalLength == -1:
            totalLength = int(round((audioLength + 500) / 1000.0))

        renderer = self.__rendererClass()
        renderer.Init(self.__profile,
                      self.__photoFilmStrip.GetAspect(),
                      outFile)

        renderer.SetAudioFiles(audioFiles)

        if self.__photoFilmStrip.GetTimelapse():
            renderEngine = RenderEngineTimelapse(self.__profile,
                                                 self.__photoFilmStrip.GetPictures(),
                                                 self.__draftMode)
        else:
            renderEngine = RenderEngineSlideshow(self.__profile,
                                                 self.__photoFilmStrip.GetPictures(),
                                                 self.__draftMode,
                                                 totalLength)

        name = "%s (%s)" % (self.__photoFilmStrip.GetName(),
                            self.__profile.GetName())

        self.__renderJob = RenderJob(name, renderer,
                                     renderEngine.GetTasks())

    def GetRenderJob(self):
        return self.__renderJob
