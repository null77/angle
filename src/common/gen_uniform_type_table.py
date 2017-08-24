#!/usr/bin/python
# Copyright 2017 The ANGLE Project Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# gen_uniform_type_table.py:
#  Code generation for OpenGL uniform type info tables.

from datetime import date

import sys

all_uniform_types = [
    "GL_NONE",
    "GL_BOOL",
    "GL_BOOL_VEC2",
    "GL_BOOL_VEC3",
    "GL_BOOL_VEC4",
    "GL_FLOAT",
    "GL_FLOAT_MAT2",
    "GL_FLOAT_MAT2x3",
    "GL_FLOAT_MAT2x4",
    "GL_FLOAT_MAT3",
    "GL_FLOAT_MAT3x2",
    "GL_FLOAT_MAT3x4",
    "GL_FLOAT_MAT4",
    "GL_FLOAT_MAT4x2",
    "GL_FLOAT_MAT4x3",
    "GL_FLOAT_VEC2",
    "GL_FLOAT_VEC3",
    "GL_FLOAT_VEC4",
    "GL_IMAGE_2D",
    "GL_IMAGE_2D_ARRAY",
    "GL_IMAGE_3D",
    "GL_IMAGE_CUBE",
    "GL_INT",
    "GL_INT_IMAGE_2D",
    "GL_INT_IMAGE_2D_ARRAY",
    "GL_INT_IMAGE_3D",
    "GL_INT_IMAGE_CUBE",
    "GL_INT_SAMPLER_2D",
    "GL_INT_SAMPLER_2D_ARRAY",
    "GL_INT_SAMPLER_2D_MULTISAMPLE",
    "GL_INT_SAMPLER_3D",
    "GL_INT_SAMPLER_CUBE",
    "GL_INT_VEC2",
    "GL_INT_VEC3",
    "GL_INT_VEC4",
    "GL_SAMPLER_2D",
    "GL_SAMPLER_2D_ARRAY",
    "GL_SAMPLER_2D_ARRAY_SHADOW",
    "GL_SAMPLER_2D_MULTISAMPLE",
    "GL_SAMPLER_2D_RECT_ANGLE",
    "GL_SAMPLER_2D_SHADOW",
    "GL_SAMPLER_3D",
    "GL_SAMPLER_CUBE",
    "GL_SAMPLER_CUBE_SHADOW",
    "GL_SAMPLER_EXTERNAL_OES",
    "GL_UNSIGNED_INT",
    "GL_UNSIGNED_INT_ATOMIC_COUNTER",
    "GL_UNSIGNED_INT_IMAGE_2D",
    "GL_UNSIGNED_INT_IMAGE_2D_ARRAY",
    "GL_UNSIGNED_INT_IMAGE_3D",
    "GL_UNSIGNED_INT_IMAGE_CUBE",
    "GL_UNSIGNED_INT_SAMPLER_2D",
    "GL_UNSIGNED_INT_SAMPLER_2D_ARRAY",
    "GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE",
    "GL_UNSIGNED_INT_SAMPLER_3D",
    "GL_UNSIGNED_INT_SAMPLER_CUBE",
    "GL_UNSIGNED_INT_VEC2",
    "GL_UNSIGNED_INT_VEC3",
    "GL_UNSIGNED_INT_VEC4"
]

# Uniform texture types.
texture_types = {"2D":"2D", "CUBE": "CUBE_MAP", "2D_ARRAY": "2D_ARRAY", "3D": "3D", "MULTISAMPLE": "MULTISAMPLE", "RECT": "RECTANGLE"}

template_cpp = """// GENERATED FILE - DO NOT EDIT.
// Generated by {script_name}.
//
// Copyright {copyright_year} The ANGLE Project Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// Uniform type info table:
//   Metadata about a particular uniform format, indexed by GL type.

#include <array>
#include "common/utilities.h"

using namespace angle;

namespace gl
{{

namespace
{{
constexpr std::array<UniformTypeInfo, {total_count}> kInfoTable =
{{{{
{uniform_type_info_data}
}}}};

size_t GetTypeInfoIndex(GLenum uniformType)
{{
    switch (uniformType)
    {{
{uniform_type_index_cases}
        default:
            UNREACHABLE();
            return 0;
    }}
}}
}}  // anonymous namespace

const UniformTypeInfo &GetUniformTypeInfo(GLenum uniformType)
{{
    return kInfoTable[GetTypeInfoIndex(uniformType)];
}}

}}  // namespace gl
"""

type_info_data_template = """{{{type}, {component_type}, {texture_type}, {transposed_type}, {bool_type}, {rows}, {columns}, {components}, {component_size}, {internal_size}, {external_size}, {is_sampler}, {is_matrix}, {is_image} }}"""
type_index_case_template = """case {enum_value}: return {index_value};"""

def cpp_bool(value):
    return "true" if value else "false"

def get_component_type(uniform_type):
    if uniform_type.find("GL_BOOL") == 0:
        return "GL_BOOL"
    elif uniform_type.find("GL_FLOAT") == 0:
        return "GL_FLOAT"
    elif uniform_type.find("GL_INT") == 0:
        return "GL_INT"
    elif uniform_type.find("GL_UNSIGNED_INT") == 0:
        return "GL_UNSIGNED_INT"
    elif uniform_type == "GL_NONE":
        return "GL_NONE"
    else:
        return "GL_INT"

def get_texture_type(uniform_type):
    for sampler_type, tex_type in texture_types.items():
        if sampler_type in uniform_type:
            return "GL_TEXTURE_" + tex_type
    return "GL_NONE"

def get_transposed_type(uniform_type):
    if "_MAT" in uniform_type:
        if "x" in uniform_type:
            return "GL_FLOAT_MAT" + uniform_type[-1] + "x" + uniform_type[uniform_type.find("_MAT")+4]
        else:
            return uniform_type
    else:
        return "GL_NONE"

def get_bool_type(uniform_type):
    if uniform_type == "GL_INT" or uniform_type == "GL_UNSIGNED_INT" or uniform_type == "GL_FLOAT":
        return "GL_BOOL"
    elif "_VEC" in uniform_type:
        return "GL_BOOL_VEC" + uniform_type[-1]
    else:
        return "GL_NONE"

def get_rows(uniform_type):
    if uniform_type == "GL_NONE":
        return "0"
    elif "_MAT" in uniform_type:
        return uniform_type[-1]
    else:
        return "1"

def get_columns(uniform_type):
    if uniform_type == "GL_NONE":
        return "0"
    elif "_VEC" in uniform_type:
        return uniform_type[-1]
    elif "_MAT" in uniform_type:
        return uniform_type[uniform_type.find("_MAT") + 4]
    else:
        return "1"

def get_components(uniform_type):
    return str(int(get_rows(uniform_type)) * int(get_columns(uniform_type)))

def get_component_size(uniform_type):
    component_type = get_component_type(uniform_type)
    if (component_type) == "GL_BOOL":
        return "sizeof(GLint)"
    elif (component_type) == "GL_FLOAT":
        return "sizeof(GLfloat)"
    elif (component_type) == "GL_INT":
        return "sizeof(GLint)"
    elif (component_type) == "GL_UNSIGNED_INT":
        return "sizeof(GLuint)"
    elif (component_type) == "GL_NONE":
        return "0"
    else:
        raise "Invalid component type: " + component_type

def get_internal_size(uniform_type):
    return get_component_size(uniform_type) + " * " + str(int(get_rows(uniform_type)) * 4)

def get_external_size(uniform_type):
    return get_component_size(uniform_type) + " * " + get_components(uniform_type)

def get_is_sampler(uniform_type):
    return cpp_bool("_SAMPLER_" in uniform_type)

def get_is_matrix(uniform_type):
    return cpp_bool("_MAT" in uniform_type)

def get_is_image(uniform_type):
    return cpp_bool("_IMAGE_" in uniform_type)

def gen_type_info(uniform_type):
    return type_info_data_template.format(
        type = uniform_type,
        component_type = get_component_type(uniform_type),
        texture_type = get_texture_type(uniform_type),
        transposed_type = get_transposed_type(uniform_type),
        bool_type = get_bool_type(uniform_type),
        rows = get_rows(uniform_type),
        columns = get_columns(uniform_type),
        components = get_components(uniform_type),
        component_size = get_component_size(uniform_type),
        internal_size = get_internal_size(uniform_type),
        external_size = get_external_size(uniform_type),
        is_sampler = get_is_sampler(uniform_type),
        is_matrix = get_is_matrix(uniform_type), 
        is_image = get_is_image(uniform_type))

def gen_type_index_case(index, uniform_type):
    return "case " + uniform_type + ": return " + str(index) + ";"

uniform_type_info_data = ",\n".join([gen_type_info(uniform_type) for uniform_type in all_uniform_types])
uniform_type_index_cases = "\n".join([gen_type_index_case(index, uniform_type) for index, uniform_type in enumerate(all_uniform_types)])

with open('uniform_type_info_autogen.cpp', 'wt') as out_file:
    output_cpp = template_cpp.format(
        script_name = sys.argv[0],
        copyright_year = date.today().year,
        total_count = len(all_uniform_types),
        uniform_type_info_data = uniform_type_info_data,
        uniform_type_index_cases = uniform_type_index_cases)
    out_file.write(output_cpp)
    out_file.close()