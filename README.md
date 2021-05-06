# PhyloSeqFilter
# Language: Python
# Input: TXT (keyword-value pairs)
# Output: PREFIX
# Tested with: PluMA 1.1, Python 3.6
# Dependency:

PluMA plugin that takes PhyloSeq-compatible OTU and TAX tables and
removes all taxa not present in at least a percentage of the samples,
which is user-specified.

The plugin takes as input a parameter file of keyword-value pairs:
OTU: OTU table (input)
TAX: TAX table (input)
META: Metadata (input)
threshold: Minimum percnetage threshold to keep taxa
OTUFilter: Filtered OTU table (output)
TAXFilter: Filtered TAX table (output)

OTUFilter and TAXFilter files will be generated with "scarce" taxa
removed, prefixed by the user-specified PREFIX.
