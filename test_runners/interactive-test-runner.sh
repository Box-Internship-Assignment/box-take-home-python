#!/bin/bash

echo "Running iteractive test runner."

USE_M=false
while getopts "m" opt; do
  case $opt in
    m) USE_M=true ;;
    \?) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
  esac
done

if ! $USE_M ; then
    echo "Use -m option when running on Mac"
fi

# setup variables
cmd=$(cat .command)
cmd=${cmd/-f/-i}
interactiveTestExpected="test_cases/interactiveModeTest.out"
interactiveTestOutFile="interactiveTestResult.out"
move1="move e1 e2"
move2="move a5 b4"

# run boxshogi and capture output
# if you see timeout errors, that means your program did not prompt for lower and UPPER turns as expected
# or that the illegal move $move2 didn't fail as it should
expect <<EOF > $interactiveTestOutFile
  spawn $cmd
  expect "lower>" { send "$move1\r" }
  expect "UPPER>" { send "$move2\r" }
  expect eof
EOF
if $USE_M; then
  SED_ARG="-i ''"  # Add the '' for macOS compatibility
else
  SED_ARG="-i"  # Don't add '' (works on Linux)
fi
# remove shogi command from output file
sed $SED_ARG '1d' $interactiveTestOutFile
# remove carriage returns from output file
sed $SED_ARG 's/\r//' $interactiveTestOutFile

# Run the diff comparison
if diff -q $interactiveTestExpected $interactiveTestOutFile; then
    echo "✅ Interactive mode test succesful."
    exit 0
else
    diff -y $interactiveTestExpected $interactiveTestOutFile
    movesToTest=$(echo "$testInputs" | sed 's/\\n/ /g')
    echo "❌ Interactive mode not working as expected. See above diff."
    echo "Boot up interactive mode and run commands $move1 and $move2. Compare to $interactiveTestExpected to debug." 
    echo "Watch for trailing spaces and newlines." 
    exit 1
fi
