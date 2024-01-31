CKOCIEMBA_SRC = coordcube.c cubiecube.c facecube.c search.c prunetable_helpers.c
CKOCIEMBA_INCLUDE = include
CFLAGS = -std=c99 -O3
BINDIR = bin
BIN = kociemba
#GCC_PATH = 
solve: solve.c $(CKOCIEMBA_SRC)
	g++ $(CFLAGS) $(CKOCIEMBA_SRC) -I$(CKOCIEMBA_INCLUDE) solve.c -o $(BINDIR)/$(BIN)
