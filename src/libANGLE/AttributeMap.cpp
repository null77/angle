//
// Copyright (c) 2014 The ANGLE Project Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//

#include "libANGLE/AttributeMap.h"

namespace egl
{

AttributeMap::AttributeMap()
{
}

void AttributeMap::insert(EGLAttrib key, EGLAttrib value)
{
    mAttributes[key] = value;
}

bool AttributeMap::contains(EGLAttrib key) const
{
    return (mAttributes.find(key) != mAttributes.end());
}

EGLAttrib AttributeMap::get(EGLAttrib key, EGLAttrib defaultValue) const
{
    auto iter = mAttributes.find(key);
    return (mAttributes.find(key) != mAttributes.end()) ? iter->second : defaultValue;
}

EGLint AttributeMap::getAsInt(EGLint key, EGLint defaultValue) const
{
    return static_cast<EGLint>(get(static_cast<EGLAttrib>(key), static_cast<EGLAttrib>(defaultValue)));
}

AttributeMap::const_iterator AttributeMap::begin() const
{
    return mAttributes.begin();
}

AttributeMap::const_iterator AttributeMap::end() const
{
    return mAttributes.end();
}

// static
AttributeMap AttributeMap::CreateFromIntArray(const EGLint *attributes)
{
    AttributeMap map;
    if (attributes)
    {
        for (const EGLint *curAttrib = attributes; curAttrib[0] != EGL_NONE; curAttrib += 2)
        {
            map.insert(static_cast<EGLAttrib>(curAttrib[0]), static_cast<EGLAttrib>(curAttrib[1]));
        }
    }
    return map;
}

// static
AttributeMap AttributeMap::CreateFromAttribArray(const EGLAttrib *attributes)
{
    AttributeMap map;
    if (attributes)
    {
        for (const EGLAttrib *curAttrib = attributes; curAttrib[0] != EGL_NONE; curAttrib += 2)
        {
            map.insert(curAttrib[0], curAttrib[1]);
        }
    }
    return map;
}
}
