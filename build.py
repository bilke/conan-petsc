from conan.packager import ConanMultiPackager
import copy
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager(archs = ["x86_64"])
    builder.add_common_builds(pure_c=True)
    builder.run()
