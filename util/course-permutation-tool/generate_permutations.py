#!/usr/bin/env python
# other comment about how this file works, plus probably an example of implementation

import json
import argparse
from argparse import ArgumentParser
from pprint import pprint
from itertools import product
from itertools import permutations
import sys
import json
import datetime
import pytz


def parse_field_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fields', nargs="*", action="append", default=None,
                        help="Specify which fields to generate permutations on")
    parser.add_argument('filename')

    num_args = parser.parse_args()

    file = open(num_args.filename)
    file_data = json.load(file)

    default_data = file_data["default_data"]
    permutation_data = file_data["permutation_data"]

    default_data_keys = permutation_data.keys()

    fields = {}

    # if no field arguments are given, just print out default data
    if not num_args.fields:
        default_permutation = file_data["default_data"]
        fields = default_permutation
    else:
        field_length = len(num_args.fields[0])

        if (field_length > 3):
            raise argparse.ArgumentTypeError("--fields can only take a max of 3 values")

        for permutation_choices in num_args.fields:
            for i in range(0, field_length):
                fields[permutation_choices[i]] = permutation_data[permutation_choices[i]]

        # the difference btwn all possible fields and the permutation ones
        default_fields = list(set(default_data_keys) - set(num_args.fields[0]))

        # add non permutation fields
        for j in range(0, len(default_fields)):
            fields[default_fields[j]] = default_data[default_fields[j]]

    return fields


def generate_permutations(fields, index, results, current, fields_dict):
    all_permutations_keys = fields.keys()
    permutation_option = all_permutations_keys[index]

    permutations_values = fields[permutation_option]

    for i in range(len(permutations_values)):
        # add other required default fields to dict
        current["number"] = "123" # will be generated automatically by course creation script
        current["organization"] = "RITX"
        current["run"] = "3T2017"
        current["user"] = "edx@example.com"
        current["partner"] = "edx"

        # configure enrollment seat settings
        enrollment_dict = {}
        enrollment_dict["credit"] = False
        enrollment_dict["credit_provider"] = "test-credit-provider"
        # enrollment_dict["audit"] = True

        # add permutation fields to dict
        fields_dict[permutation_option] = permutations_values[i]
        now = datetime.datetime.now(pytz.UTC)
        if permutations_values[i] == "future":
            future = str(now + datetime.timedelta(days=365))
            fields_dict[permutation_option] = future
        if permutations_values[i] == "past":
            past = str(now - datetime.timedelta(days=60))
            fields_dict[permutation_option] = past
        if permutations_values[i] == None:
            fields_dict[permutation_option] = None

        if all_permutations_keys[i] == "audit" and permutations_values[i] == True:
            enrollment_dict["audit"] = permutations_values[i]
        if all_permutations_keys[i] == "verify" and permutations_values[i] == True:
            enrollment_dict["verify"] = True






        if index + 1 < len(all_permutations_keys):
            generate_permutations(fields, index + 1, results, current, fields_dict)



        current["enrollment"] = enrollment_dict

        current["fields"] = fields_dict.copy()
        results.append(current.copy())
        # results["courses"] = current.copy()

    wrapper_courses_dict = {}

    wrapper_courses_dict["courses"] = results
    with open("test_courses.json", "w") as outfile:
        json.dump(wrapper_courses_dict, outfile)


if __name__ == "__main__":
    parse_field_arguments()
    generate_permutations(parse_field_arguments(), 0, [], {}, {})
