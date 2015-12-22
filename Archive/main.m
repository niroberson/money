clear, clc
% Read in the nodes and relationships files
nodes = readtable('concept.csv');
rels = readtable('Predication_aggregate2.csv');

%% Load data and extract
subject_column = 6
subject_cui = table2array(rels(:, 6));

object_column = 10;
object_cui = table2array(rels(:, 10));

concepts = table2array(nodes(:, [2, 4]));

%% Get node of interest information
% Get a random subject i.e. #100
cui_of_interest = subject_cui{100};

% Extract the name of this concept
concept_of_interest = concepts(strcmp(concepts(:,1), cui_of_interest), 2);
fprintf('CUI: %s, Concept of Interest: %s\n', cui_of_interest, concept_of_interest{:})

% Get the relationships that describe this concept
[object_rels, subject_rels] = get_rels(cui_of_interest, object_cui, subject_cui);

% Get unique primary nodes
primary_nodes = unique({object_rels{:} subject_rels{:}});

%% Compute the KSP for each primary node
% Get the number of total relationships of the search node
N_i = numel(primary_nodes);

% Get the number of total relationships of each primary node
d = [];
for j=1:N_i
    cui_j = primary_nodes{j};
    N_i_j = sum(strcmp(subject_rels,cui_j)) + sum(strcmp(object_rels, cui_j)); % Number of relationships between i and j
    [object_rels_j, subject_rels_j] = get_rels(cui_j, object_cui, subject_cui);
    N_j = numel(object_rels_j) + numel(subject_rels_j);
    
    % Calculate KSP
    KSP = N_i_j/(N_i+N_j-N_i_j);
    
    % Calculate distance of each node from KSP
    d(j) = 1/KSP - 1;
end

%% Extract cui/concept_name/distance
concept_names_idx = cellfun(@(x) find(strcmp(concepts(:,1), x)), primary_nodes, 'UniformOutput', false);
concept_names_idx = [concept_names_idx{:}];
concept_names = concepts(concept_names_idx, 2);
% Sort by distance, concept names by the distance
[d, perm] = sort(d);
concept_names = concept_names(perm);
for n=1:N_i
fprintf('Concept: %s, Distance: %0.1f\n', concept_names{n}, d(n))
end