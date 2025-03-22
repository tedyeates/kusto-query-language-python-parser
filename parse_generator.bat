cd parse_tools
antlr4 -Dlanguage=Python3 ../grammar/Kql.g4 -listener -visitor
cd ..