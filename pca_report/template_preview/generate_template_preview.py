#!/usr/bin/env python3

"""Create a PDF preview of PCA templates.

Usage:
  pca-template-preview [options] (--file FILENAME | TEMPLATE_ID...)
  pca-template-preview (-h | --help)
  pca-template-preview --version

Options:
  -d --debug                     Keep intermediate files for debugging.
  -f FILENAME --file=FILENAME    Read template IDs from a file.
  -h --help                      Show this screen.
  -s SECTION --section=SECTION   Configuration section to use.
  --version                      Show version.
"""

from docopt import docopt

args = docopt(__doc__, version="v0.0.1")
from pca.db.database import connect_from_config

connect_from_config(
    args["--section"]
)  # Must connect to the DB before we can import our MongoModels
from pca.db.database_model import *

# standard python libraries
import sys
import os
import copy
from datetime import datetime
import json
import codecs
import tempfile
import shutil
import subprocess
import re

# third-party libraries (install with pip)
import pymongo
from pymodm.errors import DoesNotExist
import pystache
from bson import ObjectId
from bson.errors import InvalidId

MUSTACHE_FILE = "template_preview.mustache"
REPORT_JSON = "template_preview.json"
REPORT_PDF = "template_preview.pdf"
REPORT_TEX = "template_preview.tex"
ASSETS_DIR_SRC = "../assets"
ASSETS_DIR_DST = "assets"
LATEX_ESCAPE_MAP = {
    "$": "\\$",
    "%": "\\%",
    "&": "\\&",
    "#": "\\#",
    "_": "\\_",
    "{": "\\{",
    "}": "\\}",
    "[": "{[}",
    "]": "{]}",
    "'": "{'}",
    "\\": "\\textbackslash{}",
    "~": "\\textasciitilde{}",
    "<": "\\textless{}",
    ">": "\\textgreater{}",
    "^": "\\textasciicircum{}",
    "`": "{}`",
    "\n": "\\newline{}",
}


class PreviewGenerator(object):
    def __init__(self, template_id_list, debug=False):
        self.__generated_time = datetime.utcnow()
        self.__results = dict()  # reusable query results
        self.__template_id_list = template_id_list
        self.__templates = list()
        self.__debug = debug

    def __run_queries(self):
        self.__templates = list(
            TemplateDoc.objects.raw({"_id": {"$in": self.__template_id_list}})
            .project({"_id": 0})
            .order_by([("complexity", pymongo.ASCENDING), ("name", pymongo.ASCENDING)])
        )

    def generate_template_preview(self):
        print(" running DB queries")
        # access database and cache results
        self.__run_queries()

        # create a working directory
        original_working_dir = os.getcwd()
        if self.__debug:
            temp_working_dir = tempfile.mkdtemp(dir=original_working_dir)
        else:
            temp_working_dir = tempfile.mkdtemp()
        os.chdir(temp_working_dir)

        # setup the working directory
        self.__setup_work_directory(temp_working_dir)

        # print ' generating attachments'
        # # generate attachments
        # self.__generate_attachments()

        # print ' generating charts'
        # # generate chart PDFs
        # self.__generate_charts()

        # generate json input to mustache
        self.__generate_mustache_json(REPORT_JSON)

        # generate latex json + mustache
        self.__generate_latex(MUSTACHE_FILE, REPORT_JSON, REPORT_TEX)

        print(" assembling PDF")
        # generate report figures + latex
        self.__generate_final_pdf()

        # revert working directory
        os.chdir(original_working_dir)

        # copy report and json file to original working directory
        # and delete working directory
        if not self.__debug:
            src_filename = os.path.join(temp_working_dir, REPORT_PDF)
            timestamp = self.__generated_time.isoformat().replace(":", "").split(".")[0]
            dest_filename = "PCA_Template_Preview-%s.pdf" % (timestamp)
            shutil.move(src_filename, dest_filename)
            shutil.rmtree(temp_working_dir)

        return self.__results

    def __setup_work_directory(self, work_dir):
        me = os.path.realpath(__file__)
        my_dir = os.path.dirname(me)
        for n in [MUSTACHE_FILE]:  # add other files as needed
            file_src = os.path.join(my_dir, n)
            file_dst = os.path.join(work_dir, n)
            shutil.copyfile(file_src, file_dst)
        # copy static assets
        dir_src = os.path.join(my_dir, ASSETS_DIR_SRC)
        dir_dst = os.path.join(work_dir, ASSETS_DIR_DST)
        shutil.copytree(dir_src, dir_dst)

    ###############################################################################
    # Utilities
    ###############################################################################

    def __latex_escape(self, to_escape):
        return "".join([LATEX_ESCAPE_MAP.get(i, i) for i in to_escape])

    def __latex_escape_structure(self, data):
        """assumes that all sequences contain dicts"""
        if isinstance(data, dict):
            for k, v in data.items():
                if k.endswith("_tex"):  # skip special tex values
                    continue
                if isinstance(v, str):
                    data[k] = self.__latex_escape(v)
                else:
                    self.__latex_escape_structure(v)
        elif isinstance(data, (list, tuple)):
            for i in data:
                self.__latex_escape_structure(i)

    ###############################################################################
    #  Attachment Generation
    ###############################################################################
    def __generate_attachments(self):
        pass

    ###############################################################################
    # Chart PDF Generation
    ###############################################################################
    def __generate_charts(self):
        pass

    ###############################################################################
    # Final Document Generation and Assembly
    ###############################################################################
    def __generate_mustache_json(self, filename):
        result = {"generated_date_tex": self.__generated_time.strftime("{%d}{%m}{%Y}")}
        result["templates"] = list()
        for template in self.__templates:
            result["templates"].append(template.to_son().to_dict())

        self.__latex_escape_structure(result["templates"])

        with open(filename, "w") as out:
            out.write(json.dumps(result))

    def __generate_latex(self, mustache_file, json_file, latex_file):
        renderer = pystache.Renderer()
        template = codecs.open(mustache_file, "r", encoding="utf-8").read()

        with codecs.open(json_file, "r", encoding="utf-8") as data_file:
            data = json.load(data_file)

        r = pystache.render(template, data)
        with codecs.open(latex_file, "w", encoding="utf-8") as output:
            output.write(r)

    def __generate_final_pdf(self):
        if self.__debug:
            output = sys.stdout
        else:
            output = open(os.devnull, "w")

        return_code = subprocess.call(
            ["xelatex", REPORT_TEX], stdout=output, stderr=subprocess.STDOUT
        )
        assert return_code == 0, "xelatex return code was %s" % return_code


def main():
    raw_template_ids = list()
    if args["--file"]:
        with open(args["--file"]) as f:
            for line in f:
                raw_template_ids.append(line.strip())
    else:  # read list of TEMPLATE_IDs from command line
        raw_template_ids = args["TEMPLATE_ID"]

    templates = list()
    for template_id in raw_template_ids:
        try:
            TemplateDoc.objects.raw({"_id": ObjectId(template_id)}).first()
        except InvalidId:
            print("Template ID is invalid: {}".format(line.strip()))
            sys.exit(-1)
        except DoesNotExist:
            print("Template ID does not exist in database: {}".format(template_id))
            sys.exit(-1)
        templates.append(ObjectId(template_id))

    if templates:
        print("Generating Template Preview for {} templates...".format(len(templates)))
        generator = PreviewGenerator(templates, debug=args["--debug"])
        results = generator.generate_template_preview()
        print("Done")
    else:
        print("No valid template IDs provided - exiting!")

    sys.exit(0)
    # import IPython; IPython.embed() #<<< BREAKPOINT >>>
    # sys.exit(0)


if __name__ == "__main__":
    main()
