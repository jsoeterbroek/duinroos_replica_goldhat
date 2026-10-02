CXX := g++
CXXFLAGS := -std=c++17 -Wall -Wno-unused-variable \
            -Iinclude -Itest -Iexternal/doctest -I.pio/libdeps/m5stack-cores3/doctest/doctest

# Source and test file detection
SRC := $(wildcard src/cal*.cpp) src/astro.cpp src/venus.cpp src/moon.cpp
TESTS := $(wildcard test/test_cal*.cpp)
OBJS := $(patsubst test/%.cpp, build/%, $(TESTS))

# Set default goal
.DEFAULT_GOAL := run

.PHONY: all clean run build goldhat

# Build everything
all: | build $(OBJS)

# Ensure build directory exists
build:
	@mkdir -p build

# Pattern rule to compile each test into build/
build/%: test/%.cpp $(SRC)
	$(CXX) $(CXXFLAGS) $^ -o $@

# Run all tests
run: all
	@for test in $(OBJS); do \
		echo "Running $$test"; \
		./$$test || exit 1; \
	done

# Manual test targets for individual calendars
goldhat: build/test_cal_goldhat
	./$<

# Clean build artifacts
clean:
	rm -rf build
