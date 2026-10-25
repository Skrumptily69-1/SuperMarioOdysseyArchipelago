#pragma once

#include "al/hio/HioNode.h"

namespace al {
class ByamlIter;
class ByamlWriter;
}  // namespace al

class ByamlSave : public al::HioNode {
public:
    virtual void write(al::ByamlWriter* writer) = 0;
    virtual void read(const al::ByamlIter& save) = 0;
};
