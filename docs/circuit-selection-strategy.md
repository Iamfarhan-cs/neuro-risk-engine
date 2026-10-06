# Circuit Selection Strategy

## 1. Objective

Task 3 defines a scientifically defensible strategy for selecting a Drosophila circuit/subgraph from the FlyWire FAFB v783 connectome for the Neuro-Risk Engine experiment.

This task is investigation and design only. It does not implement an SNN, financial features, synthetic financial data, model training, benchmarking, or the final graph representation.

The purpose of the selected topology is to provide a biological wiring constraint that can later be tested as a computational architecture. The topology is **not** assumed to encode financial-risk knowledge.

## 2. Research question

> If the full Drosophila connectome is too large and biologically detailed for the first experiment, what principled circuit/subgraph should we extract, and how can that selection be made reproducible and scientifically defensible?

The selection must be based on biological and connectomic criteria defined before the financial experiments are evaluated.

## 3. Why circuit selection matters

The FlyWire FAFB v783 connectome contains 139,255 proofread neurons and millions of synaptic connections. The published whole-brain graph is therefore substantially larger than is necessary for a first controlled topology experiment.

A subgraph is a graph containing a selected subset of neurons and the connections retained between them. In this project, the subgraph is intended to preserve a biologically meaningful piece of the fly's wiring rather than an arbitrary collection of nodes.

Selection matters for three reasons:

1. **Computational feasibility.** A smaller graph permits controlled experimentation on the available hardware.
2. **Interpretability.** A literature-defined circuit gives the topology a biological meaning that can be explained independently of financial performance.
3. **Experimental validity.** If the circuit is selected because it looks promising for the financial task, topology selection becomes part of model tuning and can introduce circular reasoning.

The whole-brain FlyWire resource also provides anatomical region, cell-type, neurotransmitter and connectivity annotations, making biologically constrained extraction possible.

## 4. Candidate selection strategies

### 4.1 Known functional circuits

A published functional circuit can be selected using a literature-defined set of neuron classes and connectivity relationships.

**Biological justification:** The circuit has an independently studied function.

**Computational usefulness:** Its topology has a clear information-flow interpretation.

**Expected graph size:** Potentially small to medium, depending on the circuit boundary.

**Reproducibility:** High when the publication defines neuron classes and the source connectome/version is fixed.

**Data availability:** High for circuits mapped to FlyWire v783.

**Selection bias risk:** Moderate if many candidate circuits are compared and the best-looking one is selected after observing computational results.

**Suitability:** High, provided the circuit is frozen before benchmarking.

### 4.2 Sensory -> integration -> output pathway

Select a pathway that contains identifiable input, intermediate/integrative and output populations.

**Biological justification:** It preserves a meaningful flow of information through a nervous system circuit.

**Computational usefulness:** The architecture naturally supports staged/event-driven computation.

**Expected graph size:** Small to large depending on how many upstream/downstream partners are included.

**Reproducibility:** High if the endpoint neuron classes, hop depth and edge filters are pre-registered.

**Data availability:** High in FlyWire.

**Selection bias risk:** Moderate to high if the pathway is chosen because its computational structure resembles the intended financial task.

**Suitability:** High as a structural extraction principle, but the biological pathway must be chosen independently of financial performance.

### 4.3 Central-complex circuits

The Drosophila central complex contains well-studied navigation and action-related circuitry. Recent connectome and functional work has identified pathways linking head-direction representations and goal-related signals to steering-related outputs.

**Biological justification:** Central-complex circuits have experimentally supported roles in navigation and goal-directed steering.

**Computational usefulness:** The circuits contain structured convergence, recurrent/parallel organization and transformations from internal representations to action-related outputs.

**Expected graph size:** Small to medium for a focused neuron-type-defined pathway; larger if broad upstream/downstream partners are included.

**Reproducibility:** High when neuron classes and connection rules are specified.

**Data availability:** High in FAFB v783.

**Selection bias risk:** Moderate. The circuit is attractive computationally, so the project must explicitly state that it is selected for biological clarity and experimental tractability, not because navigation is presumed to resemble financial decisions.

**Suitability:** High for the first experiment.

### 4.4 Mushroom-body-related circuits

The mushroom body is a well-established learning and memory centre. Adult FlyWire work also provides access to mushroom-body neuron types and their connectivity.

**Biological justification:** Strong evidence connects mushroom-body architecture with associative learning and memory.

**Computational usefulness:** Sparse and combinatorial connectivity is potentially interesting for representation learning.

**Expected graph size:** Medium to very large depending on the selected Kenyon-cell population and upstream/downstream circuit.

**Reproducibility:** High for cell-type-defined subsets, but biological variability and the complexity of the mushroom body require care.

**Data availability:** High.

**Selection bias risk:** High if the project argues that learning/memory makes it inherently appropriate for financial prediction.

**Suitability:** Good research candidate, but less clean than the central-complex steering pathway for the first topology-selection experiment.

### 4.5 Compact neuron-type-defined subnetworks

Select a set of explicitly named neuron types and include their biologically defined partners according to a fixed rule.

**Biological justification:** The neuron types are independently defined by the connectome annotation and literature.

**Computational usefulness:** Direct control over topology size and composition.

**Expected graph size:** Small to medium.

**Reproducibility:** Very high when cell-type labels, release version and partner rules are fixed.

**Data availability:** High in FlyWire v783.

**Selection bias risk:** Moderate. The principal risk is selecting neuron types because their topology appears computationally attractive.

**Suitability:** Very high as the extraction mechanism, especially when combined with a literature-defined circuit.

### 4.6 Graph-theoretic selection

Select nodes according to degree, centrality, rich-club membership, community structure or related graph statistics.

**Biological justification:** Such measures describe structural properties of the connectome.

**Computational usefulness:** Directly targets topology characteristics.

**Expected graph size:** Easily controlled.

**Reproducibility:** High if the graph statistic and threshold are fixed.

**Data availability:** High.

**Selection bias risk:** High. Selecting nodes because they have desirable computational graph statistics can make topology selection itself a form of optimization.

**Suitability:** Useful for analysis and controls, but not preferred as the primary biological selection rule.

### 4.7 Region-based selection

Select one or more anatomical neuropils and retain neurons/connections within the region or between specified regions.

**Biological justification:** Anatomical regions are meaningful organizational units, and FlyWire provides region annotations.

**Computational usefulness:** Simple and reproducible.

**Expected graph size:** From small to very large.

**Reproducibility:** High.

**Data availability:** High.

**Selection bias risk:** Moderate to high if regions are selected after inspecting computational properties.

**Suitability:** Good as a secondary comparison or boundary definition, but less specific than a literature-defined circuit.

### 4.8 Literature-defined circuits

Use a peer-reviewed publication to define the biological pathway and then map its neuron classes into the fixed FlyWire v783 release.

**Biological justification:** Selection is externally anchored in neuroscience evidence.

**Computational usefulness:** The resulting topology has a documented biological interpretation.

**Expected graph size:** Depends on the circuit.

**Reproducibility:** High if the publication, dataset release, cell classes, partner expansion and edge threshold are recorded.

**Data availability:** High for circuits represented in FlyWire.

**Selection bias risk:** Lower than purely performance-driven selection, although the initial choice among literature-defined circuits remains a design decision.

**Suitability:** Preferred.

## 5. Whole connectome vs subgraph

| Option | Biological completeness | Computational cost | Memory requirements | Implementation complexity | Interpretability | Reproducibility | Experimental validity |
|---|---|---|---|---|---|---|---|
| Full FAFB v783 | Highest | Very high | Very high relative to first experiment | High | Low-to-medium | High | Useful but impractical as first controlled topology |
| Large brain-region subgraph | High within selected region | High | High | Medium-high | Medium | High | Good |
| Known functional circuit | Moderate | Low-medium | Low-medium | Medium | High | High | Strong |
| Compact neuron-type-defined circuit | Lower | Low | Low | Low-medium | High | Very high | Strong if biologically justified |

The full FAFB v783 graph contains 139,255 proofread neurons. The published network-analysis representation contains approximately 15.1 million weighted edges. The connectivity release is also large; the v783 Zenodo package includes an 852 MB proofread connection table and a much larger synapse table.

For a first experiment on a machine with approximately 16 GB RAM and 128 GB storage, using the entire connectome would introduce unnecessary data-management and computational complexity. It would also make it harder to isolate the effect of topology from implementation constraints.

**Recommendation:** use a compact, literature-defined, neuron-type-based subgraph.

## 6. Recommended selection approach

### 6.1 Biological anchor

The first experiment should use a **central-complex, goal-directed steering pathway** as the biological anchor.

The primary literature provides an unusually clear mapping between:

- head-direction information,
- goal-direction information,
- PFL2/PFL3 populations,
- and downstream steering-related output.

A 2024 Nature study describes PFL3R, PFL3L and PFL2 as populations connecting the head-direction system to locomotor control and reports their roles in goal-directed steering. A related Nature study describes FC2 goal-related signals and their interaction with PFL3 cells.

This makes the pathway suitable as a biological circuit candidate without claiming that navigation is equivalent to financial risk.

### 6.2 Important anti-circularity rule

The financial task must **not** determine the circuit.

Bad selection:

> Choose the circuit because its biological function sounds like financial decision-making.

Defensible selection:

> Select a documented biological circuit using criteria fixed before financial benchmarking, extract its topology from a specified connectome release, and then test whether that topology provides useful computational properties on a synthetic financial task.

The financial task is therefore an evaluation environment, not a circuit-selection mechanism.

### 6.3 Exact extraction boundary

The recommended biological starting point is the literature-defined pathway centered on:

- EPG/head-direction input,
- Delta7 intermediary head-direction circuitry where present in the documented pathway,
- FC2/goal-related input where represented in the selected literature-defined circuit,
- PFL2,
- PFL3L/PFL3R,
- and the documented downstream DNa02/DNa03 steering-related populations.

The exact FlyWire root-ID list should be resolved during the extraction implementation by mapping the published neuron classes to **FAFB v783** annotations. Task 3 does not fabricate a root-ID list.

The first implementation should include only the neuron classes and partner expansions explicitly justified by the frozen circuit definition. Arbitrary graph expansion is prohibited.

### 6.4 Circuit boundary rule

Use this deterministic order:

1. Start from the pre-registered literature-defined neuron classes.
2. Map each class to the corresponding FlyWire v783 cell-type annotation.
3. Include only neurons whose annotation satisfies the frozen class definition.
4. Include only explicitly permitted circuit partners needed to preserve the documented input -> integration -> output pathway.
5. Apply the same edge threshold to every connection.
6. Do not add nodes because they improve later financial performance.
7. Do not remove nodes because they hurt later financial performance.
8. Record every inclusion/exclusion rule before benchmarking.

If the published biological class cannot be mapped unambiguously to FlyWire v783, the ambiguity must be recorded rather than resolved by performance-driven selection.

## 7. Reproducible selection rule

### Dataset

- Source: FlyWire FAFB whole-brain connectome
- Release: v783
- Organism: adult female Drosophila melanogaster
- Primary data portal: FlyWire Codex
- Connectivity data: FlyWire v783 connectivity release
- Retrieval date: 2026-10-06 for this research decision record
- DOI for connectivity release: 10.5281/zenodo.10676866

### Neuron inclusion

A neuron is included only if:

1. It belongs to a pre-registered neuron class in the selected biological pathway; or
2. It is an explicitly permitted direct circuit partner required by the pre-registered pathway boundary.

Neuron IDs must be retained exactly as supplied by FlyWire.

### Edge inclusion

An edge is included when:

- source and target neurons are both included;
- the connection is present in the proofread connectivity release;
- the connection passes the pre-registered synapse threshold.

### Synapse threshold

The initial rule is **at least 5 synapses per neuron-neuron connection**.

This follows the whole-brain FlyWire network-analysis methodology, which used a five-synapse threshold to reduce the impact of potentially spurious weak connections and because individual synapses were not all manually proofread.

The raw synapse count must still be retained so that later experiments can compare binary connectivity, raw synapse-count weights and normalized weights without re-extracting the biological topology.

### Isolated neurons

A selected neuron with no retained edges remains in the biological selection record but should be marked as isolated. The first computational graph may exclude isolated nodes from active message passing while retaining their original IDs and exclusion reason in the extraction manifest.

### Multi-edge connections

Multiple synapses between the same neuron pair are aggregated into one directed edge with a structural synapse-count attribute.

### Self-connections

Self-connections must be recorded if present in the source data. For the first computational topology, self-loops should be excluded unless the later model specification explicitly requires them. This decision must be applied deterministically to all neurons.

### Missing or uncertain data

Do not infer missing connections.

If a neuron lacks the metadata needed to satisfy the inclusion rule, classify it as unresolved and record the reason. Do not replace missing metadata using model performance, nearest-neighbour assumptions or arbitrary manual guesses.

### Excitatory/inhibitory information

Retain neurotransmitter predictions when available, but do not use them to select the circuit. Their use in computational dynamics is a later experimental decision.

### Cell-type metadata

Retain the FlyWire cell-type annotation and the source annotation/version information.

### Coordinates

Retain anatomical coordinates if available because they support later anatomical validation and distance-based analyses. Coordinates are metadata, not an input selected because they improve financial performance.

### Determinism

The extraction must not use random sampling for biological node selection.

Any later randomized control must use explicitly recorded seeds.

## 8. Target graph size

The hardware target is approximately:

- 16 GB RAM
- 128 GB storage

Candidate sizes:

### ~100 neurons

Advantages:
- Very easy to inspect.
- Low computational burden.
- High interpretability.

Disadvantages:
- May omit important intermediate and output populations.
- Greater risk that the topology becomes an artificially tiny fragment.

**Assessment:** useful for debugging and visualization, but probably too small for the main experiment.

### ~500 neurons

Advantages:
- Still tractable.
- Allows a richer circuit while remaining interpretable.
- Reasonable scale for multiple controlled topology variants.

Disadvantages:
- May still truncate biologically meaningful partner structure depending on the selected circuit.

**Assessment:** strong target.

### ~1,000 neurons

Advantages:
- Preserves more circuit context.
- Still small relative to the whole connectome.
- Allows richer graph statistics and more meaningful topology controls.

Disadvantages:
- More memory and computation than a 100-500 node graph.
- Greater implementation complexity.

**Assessment:** strong upper target for the first experiment.

### ~5,000 neurons

Advantages:
- More biological context.

Disadvantages:
- Increases complexity substantially.
- Makes topology-control matching and interpretation harder.
- Is not necessary for establishing whether topology itself produces a measurable computational effect.

**Assessment:** defer unless later evidence requires it.

### Larger than 5,000

**Assessment:** not appropriate for the first controlled experiment.

### Recommendation

Use a **preferred target range of approximately 500-1,000 active neurons**, with approximately 100-500 treated as a valid fallback if the frozen biological circuit is naturally smaller.

This is a design target, not a rule for deleting neurons to hit a number.

**Critical rule:** if the biologically defined circuit is larger than the target range, do not prune it merely to improve computational performance. Record the actual size and reconsider the experimental scope in a new, explicitly documented decision.

Actual runtime and memory consumption must be benchmarked after the topology representation is implemented. No exact performance numbers are claimed here.

## 9. Node representation

Each retained node should preserve:

| Field | Status | Reason |
|---|---|---|
| FlyWire neuron/root ID | REQUIRED | Stable identity within the source release and reproducibility |
| Cell type | REQUIRED | Defines the biological selection and supports interpretation |
| Anatomical region/neuropil | REQUIRED | Validates anatomical scope |
| Hemilineage/superclass where available | OPTIONAL | Useful biological context |
| Neurotransmitter prediction | REQUIRED metadata / later use | Needed to preserve available biological information without making it a selection criterion |
| Anatomical coordinates | OPTIONAL but recommended | Enables later anatomical checks |
| Source release/version | REQUIRED | Reproducibility |
| Inclusion reason | REQUIRED | Auditability |

## 10. Edge representation

Each edge should preserve:

- source neuron ID;
- target neuron ID;
- directed orientation;
- synapse count;
- neuropil/context if available;
- source release;
- filtering status.

### Initial structural representation

The biological topology should retain **synapse count as an edge attribute**, while also supporting a binary adjacency view.

Three later weighting modes should remain possible:

1. Binary connectivity: edge exists = 1.
2. Raw synapse count.
3. Normalized synapse count.

No choice among these should be made based on model performance in Task 3 because no model has yet been evaluated.

This separation is important: the extraction should preserve biological information broadly enough that later experiments can compare weighting strategies without changing the underlying node/edge selection.

## 11. Biological metadata

### REQUIRED

- FlyWire root/neuron ID
- cell type
- anatomical region/neuropil
- directed source/target identity
- synapse count
- dataset release/version
- inclusion/exclusion reason

### OPTIONAL

- anatomical coordinates
- hemilineage
- superclass/classification hierarchy
- neurotransmitter prediction
- neuropil-specific connection context
- data-quality indicators available from the source

### NOT NEEDED FOR FIRST EXPERIMENT

- full electron-microscopy image volume
- complete neuron morphology/skeleton geometry
- raw synapse coordinates for every synapse
- detailed developmental lineage analyses
- any biological variable not required to reconstruct or audit the selected topology

These can be retained in source references without being embedded in the first computational graph.

## 12. Experimental controls

The topology experiment must not compare the FlyWire graph against only an arbitrary random graph.

At minimum:

### A. Connectome-derived topology

The frozen biological topology defined in this document.

### B. Degree-preserving random topology

Randomly rewire the directed graph while preserving the relevant in-degree and out-degree sequences as closely as the chosen randomization algorithm permits.

This is a particularly important control because a biological graph can outperform a random graph simply because it has a different degree distribution. A degree-preserving null asks a stronger question:

> Does the specific arrangement of connections matter beyond the degree sequence?

FlyWire network-analysis work itself uses directed degree-preserving randomization as a null model for connectome structure.

### C. Generic topology control

Use a separately specified generic topology with matched node count, edge count and, where possible, comparable structural statistics.

The exact generic topology should be frozen before benchmarking.

### D. Basic random topology

A simple random topology matched for node and edge counts should be retained as a lower-complexity baseline.

### Control matching

Controls should be matched on relevant quantities such as:

- number of active nodes;
- number of directed edges;
- connectivity density;
- and, where applicable, degree statistics.

Do not over-match so aggressively that the control becomes identical to the biological graph.

## 13. Selection-bias prevention

The biological topology must be frozen **before performance benchmarking**.

This prevents a loop such as:

1. Extract circuit A.
2. Test financial task.
3. Reject circuit A.
4. Extract circuit B.
5. Test again.
6. Report B as the chosen biological architecture.

That procedure makes circuit selection part of the optimization process and makes the final result difficult to interpret.

### Decision log requirements

Before Task 4 benchmarking, record:

- source dataset and version;
- biological circuit publication(s);
- exact neuron classes;
- mapping to FlyWire cell types;
- partner-expansion rule;
- edge threshold;
- self-loop policy;
- isolated-node policy;
- missing-data policy;
- final node count;
- final edge count;
- graph statistics;
- checksum/hash of exported topology;
- date of extraction;
- software/environment version;
- random seeds for any later randomized controls.

After this record is frozen, changes require a new explicitly documented experimental version rather than an undocumented adjustment.

## 14. Reproducibility/versioning

The topology manifest should record at least:

- dataset name: FlyWire FAFB;
- dataset version: v783;
- retrieval date;
- source URL;
- DOI;
- applicable license/use terms;
- biological circuit reference;
- neuron inclusion criteria;
- edge inclusion criteria;
- synapse threshold;
- self-loop policy;
- multi-edge aggregation policy;
- missing-data policy;
- retained metadata fields;
- final node count;
- final edge count;
- density;
- in/out-degree summary;
- connected-component summary;
- checksum/hash of the exported topology;
- extraction software version/commit;
- random seeds for randomized controls.

FlyWire's public-release guidance states that public-release data are made available under CC BY-NC 4.0. The project should follow that public-release guidance and should not assume that the data may be used commercially. The Zenodo record for the connectivity deposit has separate metadata that can appear inconsistent with the FlyWire public-release guidance; this project therefore uses the stricter FlyWire public-release terms for operational handling and attribution.

The repository should not commit the full raw FlyWire connectivity dataset.

## 15. Scientific limitations

1. **Single-brain limitation.** FAFB v783 is a reconstruction of an adult female fly brain. It is not a population-average connectome.
2. **Reconstruction uncertainty.** Automated synapse detection, segmentation and proofreading have limitations.
3. **Synapse thresholding.** A five-synapse threshold reduces weak/noisy connections but may remove biologically meaningful weak connections.
4. **Cell-type mapping uncertainty.** Literature cell classes and FlyWire annotations may not always map one-to-one.
5. **Topology is not dynamics.** A connectome specifies structural connectivity; it does not by itself specify neuron dynamics, delays, plasticity or biochemical state.
6. **Topology is not function.** A biological circuit's known function does not imply that its topology will be useful for financial risk prediction.
7. **Domain transfer.** Mapping a biological topology into a financial computational task is an experimental abstraction, not a claim about biological financial cognition.
8. **Selection effects.** Even a literature-defined circuit is a design choice. The project must therefore document the candidate-selection rationale before results are known.
9. **Control adequacy.** Randomization can control selected graph statistics but cannot prove that all biological properties have been isolated.
10. **Hardware constraint.** The proposed size range is a practical design target, not a scientifically established optimal number of neurons.

## 16. Final decision record

### Decision

**Primary source:** FlyWire FAFB v783.

**Selection strategy:** literature-defined, neuron-type-defined subgraph.

**Biological anchor:** central-complex goal-directed steering circuitry, centered on the documented head-direction/goal integration pathway involving PFL2/PFL3 populations and their explicitly documented upstream/downstream partners.

**Why:** This provides a published biological circuit with a clear information-flow interpretation, strong FlyWire compatibility, and a manageable path from sensory/internal representation through integration to action-related output.

**Target size:** approximately 500-1,000 active neurons where the frozen biological circuit naturally permits it; approximately 100-500 is acceptable if the circuit is naturally smaller.

**Important:** the target is not a pruning target. Biological inclusion rules take precedence over hitting a numerical size.

**Node metadata:** root ID, cell type, neuropil/region, release/version, inclusion reason; retain additional biological metadata where available.

**Edge representation:** directed edges with raw synapse count retained; support binary, raw-count and normalized-count views later.

**Initial edge threshold:** at least 5 synapses per neuron-neuron connection.

**Controls:** biological FlyWire topology, simple matched random topology, generic matched topology, and degree-preserving randomized topology.

**Frozen before benchmarking:** circuit definition, cell-type mapping, node inclusion, partner expansion, edge threshold, self-loop policy, isolated-node policy, metadata policy, export format, and control-generation rules.

**Not frozen in Task 3:** the SNN neuron dynamics, financial feature mapping, learning rule, training procedure, exact edge-weight normalization, benchmark hyperparameters, and evaluation results.

### What is deliberately not claimed

This decision does not claim that the central-complex circuit is biologically analogous to financial decision-making.

It does not claim that the selected topology will outperform XGBoost, an MLP, a generic SNN, or any other model.

It does not claim that the fly's navigation circuitry is a financial-risk circuit.

The hypothesis to test later is narrower:

> A biologically derived topology may provide useful computational properties when used as a constrained architecture for a synthetic sequential decision task.

## 17. Task 4 handoff

Task 4 may begin only after this document is committed.

Task 4 should implement/investigate the **topology extraction specification**, not redesign the biological selection after observing results.

Task 4 should:

1. Obtain/map the required FlyWire v783 neuron annotations.
2. Resolve the literature-defined neuron classes to FlyWire cell types/root IDs.
3. Apply the frozen inclusion rules.
4. Apply the five-synapse connection threshold.
5. Apply the documented self-loop and isolated-node policies.
6. Produce an auditable topology manifest.
7. Produce a compact graph representation without committing raw FlyWire data.
8. Calculate descriptive graph statistics.
9. Produce a checksum/hash for the extracted topology.
10. Record all source/version/filter parameters needed for regeneration.

Task 4 must not choose a different biological circuit because of expected or measured financial-model performance.

## 18. References

1. Dorkenwald, S. et al. (2024). *Neuronal wiring diagram of an adult brain*. Nature 634, 124-138. https://doi.org/10.1038/s41586-024-07558-y
2. Schlegel, P. et al. (2024). *Whole-brain annotation and multi-connectome cell typing of Drosophila*. Nature 634, 139-152. https://doi.org/10.1038/s41586-024-07686-5
3. Lin, A. et al. (2024). *Network statistics of the whole-brain connectome of Drosophila*. Nature 634. https://doi.org/10.1038/s41586-024-07968-y
4. Mussells Pires, P. et al. (2024). *Transforming a head direction signal into a goal-oriented steering command*. Nature 634. https://doi.org/10.1038/s41586-024-07039-2
5. Kim, S. S. et al. (2024). *Connectomic reconstruction predicts visual features used for navigation*. Nature 634, 181-190. https://doi.org/10.1038/s41586-024-07967-z
6. Wolff, T. et al. / related central-complex navigation literature cited by the FlyWire collection. https://www.nature.com/collections/hgcfafejia
7. FlyWire Consortium (2024). *FlyWire Whole-brain Connectome Connectivity Data*, v783. Zenodo. https://doi.org/10.5281/zenodo.10676866
8. FlyWire. *Citing guidelines for publishing with FlyWire*. https://flywire.ai/guidelines
9. FlyWire. *FlyWire Principles*. https://edit.flywire.ai/principles.html
10. Eichler, K. et al. (2017). *The complete connectome of a learning and memory centre in an insect brain*. Nature 548, 175-182. https://doi.org/10.1038/nature23455
11. Fetter, R. D. et al. (2020). *Recurrent architecture for adaptive regulation of learning in the insect brain*. Nature Neuroscience 23, 544-555. https://doi.org/10.1038/s41593-020-0607-9
12. Pospisil, D. A. et al. (2024). *The fly connectome reveals a path to the effectome*. Nature 634. https://doi.org/10.1038/s41586-024-07982-0

---

## Task 3 status

**Task 3 — COMPLETE (documentation/design only).**

No SNN, financial model, synthetic financial data, training code, benchmark code, or Task 4 implementation is included in this task.
