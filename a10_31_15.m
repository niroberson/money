% Read in the nodes and relationships files
clear, clc
nodes = readtable('concept.csv');
rels = readtable('predication_aggregate1.csv');

% Plan: create 1000 Concept Nodes, Reach: Randomly sample the population
% Create all the relationships between the chosen nodes
% Create an algorithm to search for a concept and print out the concept:
% distance results

