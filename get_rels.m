function [ object_rels, subject_rels ] = get_rels( search_cui, object_cui, subject_cui )
%get_rels Return the primary relationships for a node
%   Get the primary nodesfunction get_rels(CUI)
% Get the object/subject concepts from subject/object rels
object_rels = object_cui(strcmp(subject_cui, search_cui));
subject_rels = subject_cui(strcmp(object_cui, search_cui));
end

