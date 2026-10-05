# Task 02 — Connectome & Data-Source Investigation

**Project:** Neuro-Risk Engine
**Repository:** https://github.com/Iamfarhan-cs/neuro-risk-engine
**Branch:** `development`
**Status:** Research/documentation only
**Task:** 02 — Connectome & Data-Source Investigation

---

## 1. Research Objective

The Neuro-Risk Engine experiment asks whether a biological neural topology inspired by the *Drosophila melanogaster* connectome can provide useful computational properties for real-time financial-risk decision-making.

This task does **not** build an SNN, financial model, training pipeline, benchmark, or risk classifier. Its purpose is to establish which biological connectome source can provide a defensible topology for later experimentation.

The central distinction is:

> The connectome is a source of **network topology**, not a pretrained financial model.

The intended research chain is:

```
Drosophila connectome
        ↓
biological neurons and synaptic connectivity
        ↓
selected circuit / subgraph
        ↓
computational graph
        ↓
event-driven / spiking architecture
        ↓
synthetic financial task
```

Nothing in the selected biological dataset means that a fly neuron "understands" financial risk. Any financial computation will be introduced by our experimental encoding, neuron dynamics, learning procedure, and task definition.

---

## 2. What Is a Connectome?

A **connectome** is a wiring diagram describing neurons and their connections. At synaptic resolution, the representation can include individual synaptic contacts or aggregated neuron-to-neuron connections.

For this project, the useful abstraction is:

- **Node:** a reconstructed biological neuron.
- **Directed edge:** a presynaptic neuron connected to a postsynaptic neuron through one or more detected synaptic contacts.
- **Edge multiplicity / weight:** the number of synaptic contacts between the two neurons, where the source exposes that count.
- **Node metadata:** biological annotations such as cell type, brain region/neuropil, lineage or other labels where available.

This is an anatomical/connectomic representation. It is **not** by itself a model of neural firing, learning, memory, or behavior.

FlyWire's published connectome is reconstructed from electron-microscopy imagery. Neuron reconstructions are assembled from automatically generated segments and proofread by the FlyWire community; synapses are algorithmically detected. FlyWire also provides community annotations, hierarchical cell-type information, predicted neurotransmitter identities, and links to other biological resources. [FlyWire/Codex](https://codex.flywire.ai/about_flywire), [Dorkenwald et al., 2024](https://doi.org/10.1038/s41586-024-07558-y)

---

# 3. Candidate Connectome Sources

## 3.1 FlyWire — Female Adult Fly Brain (FAFB)

**Project:** FlyWire
**Organization:** Princeton Neuroscience Institute / FlyWire Consortium
**Organism:** *Drosophila melanogaster*
**Dataset:** FAFB, Female Adult Fly Brain
**Recommended snapshot:** v783 public release

### Primary sources

- FlyWire: https://flywire.ai/
- Codex data explorer: https://codex.flywire.ai/
- FlyWire data/about page: https://codex.flywire.ai/about_flywire
- Public-release guidelines: https://home.flywire.ai/guidelines
- Main connectome paper: Dorkenwald et al., *Neuronal wiring diagram of an adult brain*, Nature (2024): https://doi.org/10.1038/s41586-024-07558-y
- Network-statistics paper: Lin et al., *Network statistics of the whole-brain connectome of Drosophila*, Nature (2024): https://doi.org/10.1038/s41586-024-07968-y

### Availability and scale

The public FAFB v783 snapshot contains **139,255 neurons** and **3,732,460 connections** according to the current Codex dataset listing. The Nature network-statistics paper reports the v783 snapshot as containing 139,255 neurons and 2,701,601 **thresholded** connections; its analysis applied a five-synapse-per-neuron-pair threshold. These numbers are therefore not contradictory: they describe different connection filtering rules. [Codex](https://codex.flywire.ai/?dataset=fafb), [Lin et al., 2024](https://doi.org/10.1038/s41586-024-07968-y)

The FlyWire project describes the dataset at approximately 140,000 neurons and more than 50 million synapses, while the 2024 publication describes the whole adult female brain reconstruction and its associated resources. [FlyWire](https://join.flywire.ai/), [Dorkenwald et al., 2024](https://doi.org/10.1038/s41586-024-07558-y)

### Biological information

FlyWire provides:

- reconstructed neurons;
- neuron identifiers;
- synaptic connectivity;
- synapse locations;
- cell-type and hierarchical annotations;
- brain-region / neuropil information;
- community labels;
- predicted neurotransmitter identities;
- morphological information;
- links to external resources such as FlyBase and Virtual Fly Brain.

The Codex explorer exposes network graphs, pathways, neuron details, annotations, neuropils, 3-D visualization and data-download functionality. [Codex](https://codex.flywire.ai/?dataset=fafb)

### Programmatic access

FlyWire's infrastructure uses CAVE (Connectome Annotation Versioning Engine). The project documents Python access through **CAVEclient**, and FlyWire analysis tools such as `fafbseg` can query and analyze FlyWire data. CAVE supports authenticated programmatic access to connectome tables and versioned data. [FlyWire apps](https://flywire.ai/apps), [CAVEclient documentation](https://caveclient.readthedocs.io/en/latest/guide/materialization.html), [CAVE paper](https://doi.org/10.1038/s41592-024-02426-z)

### License/access

Published FlyWire data are made available under **CC BY-NC 4.0**. The public-release guidance identifies v783 as the public FAFB snapshot corresponding to the October 2023 snapshot. This non-commercial license must be respected for any future use. [FlyWire Principles](https://edit.flywire.ai/principles.html), [FlyWire public-release guidelines](https://home.flywire.ai/guidelines)

### Practical assessment

**Strong candidate.** It provides the most complete adult-fly brain topology among the considered sources and exposes the exact types of biological metadata useful for later circuit selection.

The main disadvantage is scale: a full-brain graph is substantially larger than what is needed for the first controlled experiment on a 16 GB RAM machine.

---

## 3.2 Janelia FlyEM Hemibrain

**Project:** FlyEM / hemibrain
**Organization:** HHMI Janelia Research Campus, FlyEM team, with Google collaboration
**Organism:** *Drosophila melanogaster*
**Scope:** large central-brain volume rather than the entire adult brain

### Primary sources

- Janelia project page: https://www.janelia.org/project-team/flyem/hemibrain
- Hemibrain publication: Scheffer et al., *A connectome and analysis of the adult Drosophila central brain*, eLife (2020): https://doi.org/10.7554/eLife.57443
- NeuPrint user guide: https://neuprint.janelia.org/public/neuprintuserguide.pdf

### Scale and coverage

Janelia describes the hemibrain as approximately **25,000 neurons** covering a large portion of the central fly brain. It includes important circuits such as the mushroom body and central complex, with relevance to learning, memory and navigation. [Janelia FlyEM](https://www.janelia.org/project-team/flyem/hemibrain)

The original hemibrain release was approximately a third of the fly brain by volume and contained more than 20 million identified connection sites in the original public description. [Janelia](https://www.janelia.org/news/unveiling-the-biggest-and-most-detailed-map-of-the-fly-brain-yet)

### Representation

NeuPrint represents neurons and their relationships in a graph model. A neuron-to-neuron `ConnectsTo` relationship has a **weight** corresponding to the number of synaptic contacts between the neurons; regional distributions can also be represented through `roiInfo`. Adjacency matrices can be derived from this graph. [Scheffer et al., 2020](https://elifesciences.org/articles/57443)

The NeuPrint data model also exposes neuron properties such as `bodyId`, instance/type information, presynaptic and postsynaptic counts, cell-body tract information and regional information. [NeuPrint user guide](https://neuprint.janelia.org/public/neuprintuserguide.pdf)

### Access and license

Janelia states that the hemibrain is licensed under **CC-BY** and provides NeuPrint, Python access, HTTP API access, downloadable data and CSV connection summaries. [Janelia FlyEM](https://www.janelia.org/project-team/flyem/hemibrain)

### Practical assessment

**Strong secondary candidate.** Hemibrain is considerably smaller and easier to work with than the full FlyWire brain, has mature NeuPrint tooling, and has a permissive CC-BY license.

Its limitation for this project is biological scope: it does not provide the same whole-adult-brain coverage as FlyWire FAFB. If a later experiment specifically targets a well-characterized central-brain circuit, hemibrain may be an excellent source.

---

## 3.3 Drosophila Larval Brain Connectome

**Project:** Larval Drosophila connectome
**Organization:** Janelia collaborators and research partners
**Organism:** *Drosophila melanogaster* larva

### Primary source

- Winding et al., *The connectome of an insect brain*: https://www.janelia.org/publication/the-connectome-of-an-insect-brain

The published work describes a synaptic-resolution larval brain connectome comprising **3,013 neurons and approximately 544,000 synapses**, with neuron types, hubs, feedforward/feedback pathways and cross-hemisphere and brain-nerve-cord interactions. [Winding et al., Janelia publication page](https://www.janelia.org/publication/the-connectome-of-an-insect-brain)

### Practical assessment

**Useful scientific reference, but not the preferred topology source.**

It is much smaller and therefore attractive for computational experimentation. However, the Neuro-Risk Engine specification is explicitly based on a *Drosophila* brain topology and the adult FlyWire source provides a much richer adult-brain resource. Using a larval connectome would introduce a biological-stage difference that should be justified separately.

---

## 3.4 Male CNS Connectome / MCNS

**Project:** Male CNS Connectome
**Organization:** HHMI Janelia FlyEM, University of Cambridge, MRC Laboratory of Molecular Biology and collaborators
**Organism:** male *Drosophila melanogaster*

### Primary sources

- Project page: https://male-cns.janelia.org/
- Janelia project page: https://www.janelia.org/project-team/flyem/male-cns-connectome
- Codex dataset listing: https://codex.flywire.ai/

The current project documentation describes a full male CNS resource with brain and ventral nerve cord, downloadable/programmatic data and NeuPrint/Clio exploration. The current Codex listing reports MCNS v0.9 with **166,694 neurons** and **6,239,112 connections**. [Male CNS project](https://male-cns.janelia.org/), [Codex](https://codex.flywire.ai/)

### Practical assessment

**Important future candidate, but not selected for Task 2.**

It is highly relevant for future studies involving brain-to-nerve-cord or motor pathways. However, it is a newer resource than the established FAFB v783 dataset, and using it would add sex/CNS-scope considerations that are not required by the first experiment.

---

# 4. Source Comparison

| Source | Biological scope | Approximate scale | Synaptic connectivity | Metadata | Programmatic access | License/access | Initial suitability |
|---|---|---:|---|---|---|---|---|
| **FlyWire FAFB v783** | Adult female brain | 139,255 neurons | Yes | Rich | CAVEclient, Codex, related Python tools | CC BY-NC 4.0 public release | **Recommended** |
| **Hemibrain** | Large adult central-brain volume | ~25,000 neurons | Yes | Rich | NeuPrint HTTP/Python/API, downloads | CC-BY | **Strong alternative** |
| **Larval connectome** | Larval brain | 3,013 neurons | Yes | Rich circuit annotations | Research-data access | Check dataset-specific terms | Useful reference |
| **MCNS** | Male adult brain + nerve cord | 166,694 neurons in current Codex listing | Yes | Rich and growing | NeuPrint/Codex/downloads | CC-BY stated by Janelia | Future candidate |

### Selection result

**FlyWire FAFB v783 is selected as the primary biological source for the Neuro-Risk Engine experiment.**

This selection is based on:

1. adult *Drosophila* brain coverage;
2. synaptic-resolution connectivity;
3. extensive neuron/cell-type and anatomical metadata;
4. public, versioned data;
5. documented programmatic access;
6. established peer-reviewed scientific use;
7. the ability to select smaller subgraphs without requiring the whole connectome to be simulated.

The selection does **not** mean that FlyWire is scientifically superior for every possible experiment. Hemibrain may be preferable where a compact central-brain circuit and easier CC-BY reuse are the primary requirements.

---

# 5. Understanding the Selected Connectome Representation

## 5.1 Neurons

A node represents a reconstructed biological neuron/cell in the selected FlyWire dataset.

FlyWire assigns unique identifiers to reconstructed cells and provides annotations such as cell type and hierarchical classification where available. Not every neuron necessarily has equally complete annotation. FlyWire explicitly states that completeness and accuracy of annotations continue to improve. [FlyWire/Codex](https://codex.flywire.ai/about_flywire)

Therefore:

```
biological neuron → computational node
```

is a defensible abstraction, but the computational node is **not** a complete simulation of the biological neuron.

---

## 5.2 Connections

A directed connection represents synaptic connectivity from a presynaptic neuron to a postsynaptic neuron.

Conceptually:

```
Neuron A ──synaptic contacts──> Neuron B
```

FlyWire exposes synapse annotations containing presynaptic and postsynaptic neuron identifiers and spatial information through its CAVE data infrastructure. [CAVEclient materialization documentation](https://caveclient.readthedocs.io/en/latest/guide/materialization.html)



The distinction between **individual synapses** and an aggregated **neuron-to-neuron connection** is important.

If neuron A has 8 synaptic contacts onto neuron B, the graph may be represented as:

```
A ──[8]──> B
```

rather than eight separate graph nodes.

Published FlyWire analyses commonly refer to this as a connection whose strength is the number of synaptic contacts. The exact connection count depends on filtering/thresholding. For example, one whole-brain network analysis used a minimum of five synapses per neuron pair. [Lin et al., 2024](https://doi.org/10.1038/s41586-024-07968-y)

---

## 5.3 Direction

Synaptic connectivity is directional:

```
presynaptic neuron → postsynaptic neuron
```

This direction should be preserved when converting the source into the computational graph.

---

## 5.4 Synapse Count

Synapse count is a defensible candidate for a computational edge weight because it measures the observed multiplicity of synaptic contacts between a pair of neurons.

However:

```
synapse count ≠ biological synaptic efficacy
```

A larger number of anatomical contacts does not automatically establish a proportional functional influence. Therefore, the first computational experiment should describe synapse count as **structural connectivity weight**, not as a measured biological firing weight.

This distinction is critical for scientific validity.

---

## 5.5 Confidence and Quality

FlyWire synapses are algorithmically detected and associated with confidence information. Published whole-brain analyses filtered out synapses with confidence below 50 and excluded synapses that could not be assigned to valid segments. [Lin et al., 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10402125/)

The dataset's neurons are also subject to proofreading, but the proofreading process does not mean that every individual synapse has been manually verified. This is one reason published analyses have used connection-level thresholds. [Dorkenwald et al., 2024](https://doi.org/10.1038/s41586-024-07558-y)

---

## 5.6 Brain Region / Neuropil

FlyWire provides anatomical region information and annotations. The whole-brain network analysis describes the brain as divided into 78 anatomical brain regions/neuropils. [Lin et al., 2024](https://doi.org/10.1038/s41586-024-07968-y)

This gives us a defensible way to describe where a neuron participates anatomically and can later support circuit-selection criteria.

---

## 5.7 Neuron Type

FlyWire contains community and hierarchical cell-type annotations. The 2024 whole-brain annotation work reports extensive cell typing, including coverage of the optic lobes and other brain regions. [Schlegel et al., 2024](https://doi.org/10.1038/s41586-024-07686-5)

Cell type is therefore suitable as **node metadata** where the selected neuron has a reliable annotation.

It should not be treated as a numerical neural parameter automatically.

---

# 6. Biological → Computational Mapping

The following mapping is proposed for Task 3.

| Biological concept | Computational representation | Status |
|---|---|---|
| Reconstructed neuron | Graph node | Direct abstraction |
| Presynaptic → postsynaptic relationship | Directed edge | Direct abstraction |
| Number of synaptic contacts | Edge multiplicity / structural weight | Defensible transformation |
| Neuron identifier | Stable node identifier | Direct metadata |
| Cell type | Node metadata | Direct metadata where annotated |
| Brain region / neuropil | Node metadata / grouping | Direct metadata |
| Circuit | Selected subgraph | Experimental transformation |
| Synapse locations | Optional spatial metadata | Direct data, not required initially |
| Neurotransmitter prediction | Optional node/edge metadata | Direct data, but should not be equated with effect sign without additional biological assumptions |
| 3-D morphology | Optional node attributes | Direct data; not required for first topology experiment |

### Important distinction

The first three rows are close to the biological graph itself.

The later computational model will introduce additional assumptions, for example:

- whether edge weight should be normalized;
- whether every biological neuron becomes one computational unit;
- whether neurons have identical or heterogeneous dynamics;
- how external financial events enter the graph;
- how spikes propagate;
- whether recurrent loops are retained;
- how learning changes parameters.

Those are **our model assumptions**, not facts supplied by the connectome.

---

# 7. Why Connectivity Instead of Biological Images?

The research question concerns whether **network topology** can provide useful computational properties.

A raw EM image contains biological structure, but using the image directly would turn the project into an image-processing / neuron-segmentation problem before we have even tested the topology hypothesis.

The connectome provides a much more direct representation of the property under investigation:

```
image volume
   ↓
segmentation
   ↓
neuron reconstruction
   ↓
synapse detection
   ↓
connectivity graph
```

FlyWire has already performed the expensive reconstruction and provides the resulting connectivity resource.

Therefore the experiment can isolate the topology question:

> Does this biological wiring structure provide useful computational behavior when used as the topology of an event-driven model?

This is a research-design choice, not a claim that images are unimportant biologically.

---

# 8. Whole Connectome vs Selected Subgraph

## 8.1 Whole Connectome

The full FlyWire FAFB v783 resource contains 139,255 neurons and millions of aggregated connections. The source is therefore large even before adding the state required by a spiking/event-driven simulator. [Codex](https://codex.flywire.ai/?dataset=fafb)

A full simulation would require maintaining, at minimum:

- node state;
- synaptic/edge state;
- event queues;
- incoming/outgoing adjacency;
- simulation time;
- potentially trainable parameters;
- experiment bookkeeping.

The memory requirement is therefore not determined only by the raw number of edges. A simulator can have substantial runtime and memory overhead per neuron, edge and event.

### Important hardware constraint

The current experiment is intended to run on a machine with approximately **16 GB RAM**.

I cannot confirm a safe full-connectome simulation memory budget from the dataset sources alone. A benchmark would be required to establish exact runtime and RAM usage for a particular simulator and representation.

Therefore we should **not claim that the whole connectome cannot run**. The evidence supports the narrower statement that a full-brain simulation is unnecessary for the first controlled experiment and carries substantial computational cost.

---

## 8.2 Why a Subgraph Is Scientifically Preferable for the First Experiment

The research question is not:

> Can we simulate every neuron in a fly brain?

It is:

> Can biological connectivity provide useful computational properties for financial risk decision-making?

A smaller circuit allows us to control the experiment and compare architectures while keeping the topology source biologically grounded.

A subgraph also makes it possible to perform:

- topology-preserving experiments;
- ablation studies;
- random rewiring controls;
- degree-preserving controls;
- repeated runs;
- sensitivity analysis;
- comparison against conventional baselines.

These controls are more important to the research question than maximizing the number of biological neurons.

### Recommendation

**Start with a selected, scientifically justified subgraph rather than the entire FlyWire brain.**

This is not merely a hardware optimization. It reduces experimental confounding and makes it possible to test whether the specific topology contributes to the result.

---

# 9. Candidate Circuit / Subgraph Selection Strategy

Task 3 should **not** simply choose the smallest graph.

The circuit must be selected using criteria connected to the research question.

Recommended criteria, in priority order:

## Criterion 1 — Biological completeness of the selected circuit

Prefer a circuit whose neurons and connections are relatively well characterized in the source.

Reason: incomplete or poorly annotated circuits make it harder to determine whether a computational result is caused by the topology or by missing data.

## Criterion 2 — Clear input/output organization

Prefer a circuit where there is a defensible concept of:

```
input population → internal processing → output population
```

This will later make it possible to encode synthetic financial events at defined input nodes and read a decision signal from defined output nodes without pretending that the biological circuit naturally performs the financial task.

## Criterion 3 — Functional relevance to computation

Candidate circuits should have evidence of non-trivial information processing, such as sensory integration, recurrent processing, learning-related circuitry, navigation-related circuitry, or other well-characterized computations.

The selection should cite the relevant neuroscience literature.

## Criterion 4 — Manageable graph size

The first graph should be small enough to support repeated experiments on the available hardware.

This is an engineering constraint, but it should be applied **after** biological validity criteria rather than before them.

## Criterion 5 — Topological richness

Prefer a circuit containing meaningful structure such as:

- recurrent connections;
- convergent/divergent pathways;
- heterogeneous degree distribution;
- identifiable modules;
- feedback loops.

The purpose is to test whether biological topology contributes something beyond a generic feedforward graph.

## Criterion 6 — Reproducible extraction

The circuit should be selectable using documented neuron types, regions, annotations or reproducible connectivity rules.

A manually chosen set of arbitrary neurons would introduce selection bias and be difficult for another researcher to reproduce.

---



# 10. Candidate Circuit Families for Task 3

Task 3 should investigate at least the following categories rather than selecting one immediately.

### A. Sensory-processing circuit

Advantages:

- clear external input;
- well-studied information flow;
- potentially strong connectivity structure.

Risk:

- may bias the experiment toward sensory computation that is not obviously related to financial risk.

### B. Learning / memory-related circuit

The mushroom body is a major candidate because it is well represented in hemibrain and is associated with associative learning. Janelia specifically identifies mushroom-body circuitry among important hemibrain regions. [Janelia FlyEM](https://www.janelia.org/project-team/flyem/hemibrain)

Advantages:

- strong computational motivation;
- potentially relevant to pattern/value association.

Risk:

- interpreting a learning-related biological circuit as a financial decision mechanism would still be an experimental abstraction.

### C. Central-complex / navigation-related circuit

The central complex is another candidate because hemibrain includes central-complex circuitry associated with navigation. [Janelia FlyEM](https://www.janelia.org/project-team/flyem/hemibrain)

Advantages:

- recurrent and structured computations;
- clear decision/action relevance in biological literature.

Risk:

- functional analogy to financial risk must not be overstated.

### D. Graph-theoretically selected subgraph

A subgraph could be selected by measurable topology, for example:

- high recurrence;
- modular structure;
- hubs;
- balanced input/output;
- short-path organization.

Advantages:

- directly tests topology.

Risk:

- selecting a graph because it has desirable computational properties can create circular reasoning and selection bias.

### Task 3 conclusion

Task 3 should compare these strategies and select **one circuit using predeclared biological and computational criteria** before testing its financial performance.

---

# 11. Data Acquisition Plan

The planned acquisition pipeline is:

```
FlyWire FAFB v783
        ↓
public Codex / documented data access
        ↓
small required export or API query
        ↓
raw source snapshot + provenance
        ↓
validation
        ↓
normalized neuron/connection tables
        ↓
Task 3 circuit-selection procedure
        ↓
computational graph
```

## 11.1 Raw source

Use the **public FlyWire FAFB v783** snapshot as the versioned reference.

The public-release page identifies v783 as the latest public FAFB release and states that the public data are under CC BY-NC 4.0. [FlyWire public-release guidelines](https://home.flywire.ai/guidelines)

## 11.2 Acquisition methods

Possible documented access routes include:

1. Codex web/data-download functions.
2. CAVE/CAVEclient programmatic queries.
3. FlyWire ecosystem tools such as `fafbseg`.

CAVEclient supports queries against materialized synapse tables and can request only selected columns, which is useful for avoiding unnecessary data transfer. [CAVEclient documentation](https://caveclient.readthedocs.io/en/latest/guide/materialization.html)

## 11.3 Do not download everything initially

The project should not download the full raw EM volume or every available reconstruction solely for Task 2.

For topology research, the first useful data are likely to be:

- neuron identifiers;
- neuron annotations needed for circuit selection;
- connection pairs;
- synapse counts;
- relevant anatomical metadata.

3-D meshes, raw EM imagery and complete morphology should be acquired only if a later experiment requires them.

## 11.4 Validation

Before any computational conversion, Task 3/4 should verify:

- source name;
- dataset version;
- extraction date;
- query/filter definition;
- number of neurons retrieved;
- number of connections retrieved;
- duplicate records;
- missing node IDs;
- self-connections, if present;
- direction consistency;
- weight/count validity;
- annotation coverage.

## 11.5 Reproducibility

The project should record:

```
dataset = FAFB
version = v783
source = FlyWire/Codex
query/filter = <exact Task 3 definition>
retrieval_date = <recorded at acquisition>
software_versions = <recorded at acquisition>
```

The project should never silently replace one FlyWire release with another.

---

# 12. Scientific Limitations

## 12.1 Connectome completeness

A connectome is a reconstruction of a biological specimen, not a perfect abstract representation of every neuron in every fly.

FlyWire's public dataset is a particular adult female *Drosophila* brain. Results therefore cannot automatically be generalized to every fly or every individual.

---

## 12.2 Synapse detection is not equivalent to ground truth

FlyWire synapses are algorithmically detected. Published analyses use confidence filtering and, in some analyses, connection thresholds. The whole-brain network paper explicitly notes that thresholding can undercount true connections because individual synapses were not all manually proofread. [Lin et al., 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10402125/)

Therefore:

```
observed graph ≠ perfect biological graph
```

---

## 12.3 Anatomical connectivity is not functional connectivity

An anatomical edge tells us that a synaptic contact was reconstructed.

It does not by itself establish:

- exact synaptic efficacy;
- firing probability;
- temporal dynamics;
- neuromodulatory state;
- learning state;
- context-dependent behavior.

This is one of the most important limitations of the proposed experiment.

---

## 12.4 Synapse count is not automatically synaptic strength

We may later use synapse count as a graph weight because it is an observable structural quantity.

However, that creates an abstraction:

```
synapse count
      ↓
structural weight
      ↓
computational influence
```

The final arrow is a **modeling assumption**, not a directly measured biological fact.

---

## 12.5 Temporal dynamics are largely absent from a static topology

The connectome primarily describes structural relationships.

It does not by itself provide the complete time-dependent dynamics required for a spiking neural simulation.

Task 3 onward will therefore need to define:

- neuron model;
- membrane dynamics;
- spike-generation mechanism;
- synaptic delays, if used;
- refractory behavior;
- learning/update rules.

These must be clearly marked as experimental assumptions.

---

## 12.6 Neuron abstraction

Mapping one biological neuron to one computational node simplifies biology.

A biological neuron can contain:

- complex dendritic structure;
- multiple compartments;
- nonlinear integration;
- diverse receptor mechanisms;
- neuromodulatory effects.

A simple computational node will not preserve all of this.

---

## 12.7 Circuit-selection bias

Choosing a circuit because it performs well on the financial task would invalidate a strong causal interpretation.


For this reason, Task 3 should define selection criteria **before** evaluating financial performance.


---

## 12.8 Dataset version drift

FlyWire is actively maintained. Codex states that annotations continue to be updated. Public snapshots and current production data can therefore differ. [Codex](https://codex.flywire.ai/about_flywire)

The experiment must pin a public release/version.

---

## 12.9 License constraint

FlyWire public data are under CC BY-NC 4.0. This is appropriate for a research/educational side project but creates a restriction for commercial reuse. The project must retain the required attribution and follow the current license terms. [FlyWire Principles](https://edit.flywire.ai/principles.html)

---

# 13. What the Connectome Can and Cannot Tell Us

| Question | Connectome can provide | Connectome cannot establish by itself |
|---|---|---|
| Which neurons are connected? | Yes | — |
| Direction of anatomical synaptic connectivity | Yes | — |
| Approximate synaptic multiplicity | Yes | — |
| Brain-region association | Yes, where annotated | — |
| Cell-type information | Yes, where annotated | — |
| 3-D anatomical structure | Yes, through reconstruction resources | — |
| Exact functional synaptic efficacy | No | Requires additional evidence/modeling |
| Neural firing dynamics | No | Requires a neuron model/data |
| Financial knowledge | No | Must be introduced by experiment |
| Risk understanding | No | Must be learned/evaluated computationally |
| Causal superiority over XGBoost | No | Requires controlled benchmark |
| Biological equivalence of the computational model | No | Requires much richer biological modeling |

This table is a core scientific boundary for the project.

---

# 14. Decision Record

## Recommended Connectome Source

**Name:** FlyWire FAFB v783 — Female Adult Fly Brain

### Reason

It provides an adult *Drosophila* whole-brain connectome with synaptic connectivity, extensive anatomical and cell-type metadata, public versioned access, and documented programmatic tooling.

### Evidence

- 139,255 neurons in the v783 public snapshot. [Codex](https://codex.flywire.ai/?dataset=fafb)
- Peer-reviewed whole-brain connectome publication. [Dorkenwald et al., 2024](https://doi.org/10.1038/s41586-024-07558-y)
- Documented synaptic connectivity and confidence filtering. [Lin et al., 2024](https://doi.org/10.1038/s41586-024-07968-y)
- CAVE/CAVEclient programmatic access. [CAVEclient](https://caveclient.readthedocs.io/en/latest/guide/materialization.html)
- Public data release under CC BY-NC 4.0. [FlyWire guidelines](https://home.flywire.ai/guidelines)

---

## Recommended Initial Representation

**Directed weighted graph**, where:

```
node = reconstructed neuron
edge A → B = anatomical synaptic connectivity
edge weight = synaptic-contact count, if retained
metadata = biological annotations
```

The weight must be described as a **structural connectivity measure**, not as biological synaptic efficacy.

---

## Recommended Initial Scale

**Selected subgraph, not the whole connectome.**

### Reason

The research question concerns whether connectome-derived topology provides useful computational properties. The first experiment therefore needs a tractable, reproducible and biologically defensible circuit rather than maximum biological scale.

The full FlyWire dataset is large enough that simulation cost, event management and memory overhead become meaningful engineering constraints. Exact resource requirements cannot be inferred from neuron/edge counts alone and must be benchmarked once a computational representation is defined.

---

## Recommended Selection Criteria

Task 3 should select a circuit using:

1. biological characterization;
2. clear input/output organization;
3. functional relevance to information processing;
4. reproducible extraction rules;
5. manageable size;
6. non-trivial topology;
7. minimal selection bias.

The criteria should be finalized before measuring financial-task performance.

---

## Main Risks

1. **Topology-to-function overinterpretation** — structural wiring does not automatically imply useful computation.
2. **Synapse-weight assumption** — synapse count may not equal functional strength.
3. **Dataset incompleteness/noise** — reconstruction and synapse detection have uncertainty.
4. **Circuit-selection bias** — choosing a favorable subgraph can invalidate causal claims.
5. **Model abstraction loss** — a graph omits much biological detail.
6. **Version drift** — changing connectome snapshots can change results.
7. **License constraints** — FlyWire's public release is CC BY-NC 4.0.
8. **Scale** — the full graph is unnecessary for the initial experiment and may complicate controlled evaluation.
9. **Benchmark confounding** — any observed advantage could come from parameter count, preprocessing, optimization, or other factors rather than topology.
10. **Biological analogy risk** — the project must never claim that the fly brain intrinsically performs financial-risk reasoning.

---

# 15. Answers for Recruiter / Interview Discussion

## Why did you choose a Drosophila connectome?

Because *Drosophila* provides unusually detailed publicly available neuronal wiring data at synaptic resolution. The experiment is specifically interested in whether biological network topology can provide computational properties that are useful outside conventional artificial-network architectures.

The connectome is being used as a **topology source**, not as a pretrained model.

## What exactly is a connectome?

A connectome is a wiring representation of neurons and their connections. At synaptic resolution, it can describe directed relationships between reconstructed neurons and the number/location of synaptic contacts.

## What does an edge represent?

In this experiment, an edge represents reconstructed anatomical synaptic connectivity from a presynaptic neuron to a postsynaptic neuron. If aggregated, the edge can carry the number of synaptic contacts between the two neurons.

## Why use connectivity instead of biological images?

Because the hypothesis concerns network topology. Using raw images would introduce a separate image-segmentation problem. The published connectome already converts the biological image volume into reconstructed neurons and connectivity, allowing the experiment to focus on topology.

## Why not use the entire fly brain?

The research question does not require simulating every neuron. A controlled subgraph allows repeated experiments, ablations, topology controls and comparisons on the available hardware. The whole brain is useful as the **source reservoir** from which a reproducible circuit can be selected.

## How do you convert biological connectivity into a computational graph?

Map reconstructed neurons to nodes, directed synaptic relationships to directed edges, and optionally aggregate synaptic contact counts as structural edge weights. Biological annotations become node metadata.

## What information is lost?

Detailed morphology, compartmental dynamics, neurotransmitter/receptor interactions, temporal dynamics, neuromodulation, and many other biological mechanisms are not preserved by a simple graph abstraction.

## What assumptions did you make?

The major assumptions begin after extraction:

- one biological neuron becomes one computational node;
- synapse count may be used as a structural edge weight;
- the selected subgraph is sufficient to test the topology hypothesis;
- a later computational neuron model can operate over this topology.

These assumptions must be tested rather than presented as biological facts.

## What would invalidate the experiment?

Examples include:

- selecting a circuit after seeing which one performs best;
- changing the topology without preserving experimental controls;
- comparing models with substantially different parameter budgets without accounting for it;
- claiming financial understanding from biological topology alone;
- failing to pin the connectome version;
- using undocumented or non-reproducible data filtering;
- showing an apparent performance gain that disappears under topology-matched controls or random-rewiring ablations.

---

# 16. Task 3 Handoff

Task 3 should now investigate and select the actual biological circuit/subgraph.

Task 3 should **not** begin by downloading the entire FAFB dataset.

The next investigation should answer:

1. Which candidate FlyWire circuit has the best scientific fit?
2. What exact neurons define its input and output populations?
3. What source annotations identify those neurons?
4. What reproducible query can extract the circuit?
5. What graph size results?
6. Which connections should be retained?
7. What threshold, if any, should be applied?
8. What biological literature supports the circuit's functional characterization?
9. What control subgraphs should be created for later ablation/comparison?

Only after these questions are answered should the project create a normalized topology representation.

---

# 17. References

## Primary / Official Sources

1. FlyWire — Connectomics platform: https://flywire.ai/
2. FlyWire Codex — Connectome Data Explorer: https://codex.flywire.ai/
3. FlyWire data/about page: https://codex.flywire.ai/about_flywire
4. FlyWire public-release guidelines: https://home.flywire.ai/guidelines
5. FlyWire Principles: https://edit.flywire.ai/principles.html
6. Janelia FlyEM Hemibrain: https://www.janelia.org/project-team/flyem/hemibrain
7. Janelia Male CNS Connectome: https://www.janelia.org/project-team/flyem/male-cns-connectome
8. Male CNS project: https://male-cns.janelia.org/
9. NeuPrint user guide: https://neuprint.janelia.org/public/neuprintuserguide.pdf
10. CAVEclient documentation: https://caveclient.readthedocs.io/en/latest/guide/materialization.html

## Peer-Reviewed / Scientific Sources

11. Dorkenwald et al. (2024). *Neuronal wiring diagram of an adult brain*. Nature.
https://doi.org/10.1038/s41586-024-07558-y

12. Lin et al. (2024). *Network statistics of the whole-brain connectome of Drosophila*. Nature.
https://doi.org/10.1038/s41586-024-07968-y

13. Schlegel et al. (2024). *Whole-brain annotation and multi-connectome cell typing of Drosophila*. Nature.
https://doi.org/10.1038/s41586-024-07686-5

14. Scheffer et al. (2020). *A connectome and analysis of the adult Drosophila central brain*. eLife.
https://doi.org/10.7554/eLife.57443

15. Winding et al. (2023). *The connectome of an insect brain*.
https://www.janelia.org/publication/the-connectome-of-an-insect-brain

16. CAVE: *Connectome Annotation Versioning Engine*. Nature Methods.
https://doi.org/10.1038/s41592-024-02426-z

---

## Evidence Note

Dataset counts in this document are always qualified by **dataset version and counting definition** where the sources provide different numbers.

In particular:

- Codex currently lists FAFB v783 as 139,255 neurons and 3,732,460 connections.
- Lin et al. report 2,701,601 **thresholded** connections for v783 after applying a five-synapse-per-pair threshold.
- The broader FlyWire resource describes more than 50 million individual synapses.

These quantities measure different levels of the representation and must not be treated as interchangeable.

---

## Final Scientific Boundary


The strongest defensible claim after Task 2 is:

> **FlyWire FAFB v783 is a suitable biological source from which to derive a reproducible, directed, synapse-informed topology for a research-only computational experiment.**
