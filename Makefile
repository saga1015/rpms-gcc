# Makefile for source rpm: gcc
# $Id$
NAME := gcc
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
