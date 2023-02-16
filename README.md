# bio-cmd

## Project Description

This is a site that performs some operations on a file or sequence of DNA, RNA or protein

## Operations Description

gc Usage gc seq Parameters seq : a string represents the sequence Description This operation takes a seq as a string and returns the gc percentage of it.

transcribe Usage transcribe seq

seq : a string represents the sequence Description This operation takes a seq as a string and returns its transcription.

reverse_complement Usage reverse_complement seq

seq : a string represents the sequence Description This operation takes a seq as a string and returns its reverse complement.

calc_nbases Usage calc_nbases seq

seq : a string represents the sequence Description This operation takes a seq and calculates its nbases

is_valid Usage is_valid seq type Options and arguments

seq : a string represents the sequence type : a string that represents the type of the sequence. It can be one of these keywords [protein, dna, rna]
