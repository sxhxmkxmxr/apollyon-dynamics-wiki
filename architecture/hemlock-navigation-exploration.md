# Hemlock Mk II Navigation & Terrain-Following Exploration
**Working Architecture Document · Apollyon Dynamics Engineering Wiki**
*Status: Engineering Discussion & Architectural Exploration Draft (Rev 1.0)*

---

## 1. Executive Context & The High-Subsonic Problem Statement

The **Hemlock Mk II** represents Apollyon Dynamics' long-range strategic strike effector:
- **Envelope:** 1,000–1,500 km operational range, high-subsonic cruise (900 km/h / Mach 0.73–0.75), 1,000 kg warhead class.
- **Flight Profile:** Low-altitude terrain-hugging ingress below radar horizons through multi-tiered Integrated Air Defence Systems (IADS) along contested Himalayan frontiers and littoral corridors.
- **Threat Environment:** Comprehensive electronic warfare, wide-area GNSS denial (pseudorange spoofing, high-power barrage and sweep jamming), and dense passive Electronic Support Measures (ESM) tracking RF emissions.

Achieving sub-3-metre terminal precision over a 1,500 km flight envelope under total electromagnetic contestation requires re-evaluating traditional cruise missile guidance paradigms. Historical solutions (e.g., Tomahawk, Storm Shadow, Kalibr) rely on exquisite, export-restricted hardware architectures developed in the 1980s–1990s. 

This document explores and details four foundational pillars of the Hemlock Mk II navigation architecture:
1. **Terrain-Following & Contour Matching:** Why modern edge-computed correlation against public/commercial DEMs is vastly cheaper and less detectable than legacy TERCOM.
2. **Deep Scene Matching:** Moving from fragile pixel-level cross-correlation (classical DSMAC) to invariant topological semantic embeddings.
3. **Controlled Reception Pattern Array (CRPA):** The indispensable hardware-level bulwark against multi-axis GNSS denial.
4. **The Physical Failure Modes of Visual-Inertial Odometry (VIO):** Why frame-to-frame visual odometry is not used at high-subsonic velocities, and how periodic snapshot geo-registration replaces it.

---

## 2. Terrain-Following & Contour Matching: Disrupting Legacy TERCOM

### 2.1 The Legacy TERCOM Bottleneck

Classical TERCOM (Terrain Contour Matching), pioneered on the BGM-109 Tomahawk and AGM-86, is structurally expensive, complex, and tactically vulnerable:
1. **Bespoke Military Hardware:** Legacy systems rely on narrow-band, high-power militarised radar altimeters ($80,000–$150,000 per unit) subjected to decadal mil-spec qualification cycles.
2. **Proprietary Hardware Correlators:** Early implementations used analog delay lines and specialized digital signal processors configured to correlate 1D elevation profiles against proprietary DTED (Digital Terrain Elevation Data) Level 3 matrices.
3. **Active Emission Signatures:** Traditional radar altimeters emit continuous RF energy directly beneath and ahead of the missile. Ground-based or airborne ESM (Electronic Support Measures) systems readily intercept these emissions, triangulating the missile's approach axis long before visual acquisition.
4. **Mapping Dependency:** Sourcing classified high-resolution elevation matrices across foreign sovereign territory historically required dedicated orbital reconnaissance assets and national-level mapping agencies.

### 2.2 The Hemlock Mk II Approach: Edge-Compute Terrain Correlation

Hemlock Mk II inverts this economics by taking advantage of contemporary automotive sensor industrialisation, open/commercial planetary elevation models, and high-density edge neural compute:

| Metric / Attribute | Legacy TERCOM (1980s–2000s) | Hemlock Mk II Approach |
| :--- | :--- | :--- |
| **Altimetry Hardware** | Custom militarised C-band radar altimeter ($100k+) | Automotive-class solid-state micro-radar (<₹3–5 lakh) |
| **Mapping Pipeline** | Classified military DTED Level 3/4 via national agencies | Processed global elevation sets (Copernicus, Cartosat, SRTM GL1) |
| **Correlation Engine** | Dedicated hardwired correlator boards | Parallelized matrix correlation on shared edge compute accelerators |
| **Emission Profile** | Continuous RF altimetry (detectable beacon) | **Periodic low-exposure altimetry** (pulsed only at designated navigational gates) |
| **Software Modularity** | Rigid, flight-certified embedded firmware | Containerized navigation kernel running inside shared flight OS |
| **Unit Cost Impact** | ₹1.2–2.0 Cr per munition avionics stack | <₹12–18 lakh total sensor and compute allocation |

### 2.3 Algorithmic Mechanics: Low-Duty-Cycle Matrix Correlation

Rather than continuously firing RF altimeter pulses:
1. **Inertial-Barometric Dead-Reckoning:** Hemlock Mk II flies primarily on a tightly coupled baro-inertial channel. Altitude above sea level is tracked through static pressure fused with the inertial vertical state.
2. **Terrain Gate Triggers:** Flight mission planning identifies high-gradient terrain features ("navigational gates" such as distinct ridgelines, steep river valleys, or escarpments) along the ingress route.
3. **Short Sampling Windows:** Upon arriving at an expected gate window, the altimeter samples ground clearance briefly before returning to electromagnetic silence.
4. **Bayesian Elevation Profile Matching:** The sampled elevation profile is compared against pre-cached gradient strips from the DEM. A sequential estimator computes the position correction, collapsing the inertial uncertainty ellipse.
5. **ESM Exposure:** Because emissions last a fraction of a second, hostile ESM cannot build an emitter track.

---

## 3. Scene Matching: Topological Embeddings vs Fragile Pixel Matching

### 3.1 Why Classical DSMAC Fails

Digital Scene-Mapping Area Correlators (DSMAC) traditionally took an optical snapshot of a target area and performed pixel-intensity correlation (Normalized Cross-Correlation, Mean Absolute Difference, or SSDA) against a stored reference photograph.

In operational practice across the subcontinent, this breaks down under predictable environmental variability:
- **Seasonal Invariance Failure:** A reference image captured in dry summer fails in winter under snow cover or seasonal flooding.
- **Diurnal Sun Angle & Shadow Shift:** Morning shadows cast across mountain peaks invert luminance gradients compared to afternoon reconnaissance passes.
- **Thermal Crossover:** If matching a daytime visible-spectrum satellite reconnaissance image against an onboard long-wave infrared (LWIR) terminal camera, thermal contrast inversions (e.g., concrete vs vegetation temperature flips at dusk) produce negative or zero correlation scores.

### 3.2 Deep Topological Feature Embeddings

Hemlock Mk II replaces raw pixel intensity matching with **deep structural representations** pre-trained on multi-spectral satellite imagery:

```
[ Commercial Satellite Imagery ] ──> [ Contrastive Structural Encoder ] ──> [ Compact Vector Hash (Latent Map) ]
                                                                                         │
[ Onboard Live Optical/IR Frame ] ──> [ Lightweight Edge Transformer ]  ──> [ Real-Time Feature Embedding ]
                                                                                         │
                                                                           ┌─────────────┴─────────────┐
                                                                           │ Affine Invariant Matching  │
                                                                           │ Cosine Similarity Scoring │
                                                                           └─────────────┬─────────────┘
                                                                                         │
                                                                           [ Kalman Coordinate Update ]
```

1. **Semantic Invariant Extraction:** Rather than saving pixel arrays, the offline mission preparation tool passes satellite imagery through a contrastive vision backbone. The network extracts geometric invariants:
   - Ridgeline topology and drainage basin skeletons.
   - Road junctions, railway lines, and canal vectors.
   - Structural boundary geometry of buildings and industrial compounds.
2. **Compact Onboard Footprint:** An operational scene is compressed into a compact vector embedding (compared to tens of megabytes of raw uncompressed imagery), allowing hundreds of fallback checkpoints to reside in flash memory.
3. **Cross-Modality Invariance:** Because the encoder is trained contrastively across paired visible and thermal datasets, the model matches a live LWIR thermal snapshot taken at night in fog against a daylight public optical satellite reference taken years prior.
4. **Rejection of Transient Noise:** Agricultural seasonal plowing, temporary cloud shadows, and seasonal snow cover are treated as latent high-frequency noise and discarded by the encoder, isolating solely permanent topographic structure.

---

## 4. CRPA: The Indispensable Hardware Bulwark Against GNSS Denial

Software-only anti-jam algorithms (e.g., frequency-hopping, narrow-band notch filters, or Kalman pseudorange screening) provide only limited interference suppression. In modern operational theatres, tactical electronic warfare systems deploy ground jammers within line of sight, saturating low-noise amplifiers (LNAs), driving them into nonlinear compression and blinding standard single-patch receivers.

### 4.1 Controlled Reception Pattern Array (CRPA) Architecture

**CRPA is a spatial hardware-layer defense that rejects jammers before they enter the receiver electronics.**

```
       Hostile Jammer
     (Horizon Emitter)
            \ 
             \  [Spatial Null Synthesized]
              \
        ┌──────▼──────┐
        │  Antenna 1  │
        │  Antenna 2  │ ──> [ Multi-Channel ] ──> [ FPGA / DSP ] ──> [ Clean Baseband ]
        │  Antenna 3  │     [ RF Front-End  ]     [ Null-Steering]   [ NavIC / GPS   ]
        │  Antenna 4  │     [ Downconverter ]     [ Space-Time   ]   [ Receiver Core ]
        └──────▲──────┘                           [ Adaptive Proc]
              /
             /  [High-Gain Constructive Beam]
            /
    NavIC / GPS Satellites
         (Zenith)
```

1. **Multi-Element Geometry:** Hemlock integrates a conformal multi-element microstrip patch antenna array flush into the dorsal composite skin.
2. **Space-Time Adaptive Processing (STAP / SFAP):**
   - Each antenna element feeds an independent RF receiver path.
   - The digital signal processor monitors the spatial covariance matrix across elements.
   - When jamming energy is detected, the adaptive algorithm computes complex weighting factors ($w_1, w_2, \dots, w_n$) that synthesize destructive interference (deep spatial nulls) in the direction of the jammer's arrival angle ($\theta, \phi$).
3. **Deep Null Depth:** A well-calibrated multi-element array delivers deep spatial attenuation directly toward horizon jammers.
4. **Constellation & Frequency Diversity:**
   - **NavIC Priority:** Native dual-frequency support for NavIC L5 (1176.45 MHz) and S-band (2492.028 MHz), exploiting sovereign orbital control.
   - **Multi-Constellation Fallback:** Concurrent tracking of GPS L1/L2, GLONASS G1/G2, and Galileo E1/E5a.
   - *Asymmetry:* For an adversary to deny position fix, they must emit high-power jamming across L1, L2, L5, and S-band simultaneously from multiple dispersed azimuths, massively escalating their own electronic signature and vulnerable emitter profile.

---

## 5. Why Visual-Inertial Odometry (VIO) Is Not Used at High-Subsonic Speeds

Visual-Inertial Odometry (VIO) and Visual SLAM (e.g., VINS-Mono, ROVIO, ORB-SLAM3) are standard navigation staples for small commercial drones flying at low airspeeds. However, applying frame-to-frame VIO to high-subsonic cruise missiles is a fundamental engineering mismatch.

The mathematical and physical reasons are decisive:

### 5.1 Optical Flow Displacement & Search Basin Breakdown
- At high subsonic speed, an aircraft at low altitude traverses hundreds of metres every second.
- At typical downward-camera frame rates, the vehicle moves several metres per frame.
- Traditional optical flow algorithms and feature trackers rely on small local neighbourhood searches. Large inter-frame displacement causes feature tracking to drop out entirely.
- Increasing camera frame rates to reduce per-frame pixel displacement introduces compute and memory bandwidth requirements that the thermal and SWaP budgets on an attritable missile cannot sustain.

### 5.2 Motion Blur vs Exposure Time in Contested Conditions
- To arrest pixel smearing at high speed and low altitude, shutter exposure time must be very short.
- In dawn, dusk, heavy overcast, or adverse weather missions, such exposure times require large aperture optics and extreme sensor ISO gain, injecting photon shot noise and sensor read noise that degrades corner and gradient detectors.

### 5.3 Parallax Degeneracy at Ingress Altitudes
- When the munition transits over undulating terrain at altitude, the distance to terrain features becomes large relative to the optical baseline between consecutive frames.
- Under these conditions, the essential matrix degenerates toward a homography. The camera measures angular velocity well, but translational scale (forward velocity and altitude) becomes weakly observable or mathematically unobservable without external aiding.
- The scale factor drifts rapidly, causing the filter state covariance to grow within seconds.

### 5.4 Acoustic and Aerodynamic High-Frequency Noise on MEMS IMUs
- High-subsonic flight entails violent turbulent boundary layer excitation, transonic buffet, and high-frequency acoustic noise from the turbojet intake and exhaust.
- Standard VIO depends on integrating MEMS accelerometer and gyroscope data at high rate between visual frames.
- Structural vibration leaks past mechanical isolators, aliasing into the accelerometer bias registers and producing rapid quadratic velocity drift between visual updates.

### 5.5 The Solution: Periodic Absolute Geo-Referencing, Not Continuous VIO
Because frame-to-frame VIO cannot survive these physics, Apollyon rejects visual odometry for high-subsonic cruise. 

Instead, the architecture couples:
1. **Continuous Dead-Reckoning:** Tactical MEMS IMU with barometric dampening tracks attitude and short-term accelerations smoothly.
2. **Periodic Absolute Ground Fixes:** At intervals along the route (or upon crossing pre-designated terrain waypoints), the aircraft takes an instantaneous global-shutter snapshot.
3. **Drift Correction:** The snapshot is registered against the onboard satellite topological embedding (Section 3), producing an **absolute geographic coordinate fix** rather than a relative dead-reckoned offset. This resets accumulated drift without ever integrating frame-to-frame visual errors.

---

## 6. Synthesis: The Hemlock Navigation Stack

The integrated navigation architecture for Hemlock Mk II forms a resilient, tiered defense against complete A2/AD denial:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             HEMLOCK MK II TIERED PNT                             │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  [ TIER 1: HARDWARE RF DEFENSE ]                                                 │
│  CRPA Multi-Element Antenna Array                                                │
│  ├── Deep spatial nulling against horizon ground jammers                         │
│  └── Concurrent tracking: NavIC (L5, S) + GPS (L1/L2) + Galileo (E1/E5)         │
│                                                                                  │
│  [ TIER 2: CONTINUOUS DAMPED INERTIAL BACKBONE ]                                │
│  Tactical-Grade MEMS IMU + Barometric Air Data System                            │
│  ├── High-rate attitude and velocity dead-reckoning                              │
│  └── Barometric vertical channel damping (prevents altitude divergence)          │
│                                                                                  │
│  [ TIER 3: DISCRETE TERRAIN CONTOUR FIXES (LOW-EXPOSURE) ]                      │
│  Automotive-class Solid-State Micro-Radar                                        │
│  ├── Intermittent altimetry at pre-designated elevation gates                    │
│  └── Edge matrix correlation against pre-cached Copernicus / Cartosat DEMs       │
│                                                                                  │
│  [ TIER 4: ABSOLUTE TOPOLOGICAL SCENE REGISTRATION ]                             │
│  Downward Global-Shutter Optical / LWIR Thermal Sensor                           │
│  ├── Deep topological feature embeddings invariant to seasons/lighting           │
│  └── Periodic absolute geographic reset (replaces failed continuous VIO)         │
│                                                                                  │
│  [ TIER 5: TERMINAL GUIDANCE ]                                                   │
│  Tonbo Dual-Band EO/IR Seeker (TRAP-1 Class)                                     │
│  └── Autonomous optical target geometry acquisition and kinetic terminal lock     │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Action Items & Technical Discussion Points for Engineering Team

1. **Hardware Evaluation:**
   - Procure and benchmark automotive-grade radar transceivers on the lab shaker table to measure phase noise under simulated turbojet acoustic vibration.
   - Complete anechoic chamber testing of the conformal microstrip CRPA antenna array with simulated ground jammers at low elevation angles.
2. **Algorithm & Compute Benchmarking:**
   - Benchmark the topological feature encoder on edge accelerators to verify deterministic inference budgets per scene snapshot.
   - Run simulation test runs over high-relief digital elevation sets to determine optimal spatial gate density for intermittent altimetry.
3. **Flight Trials:**
   - Test the altimeter and snapshot scene matching stack on the Nightshade Mk II testbed before integrating onto Hemlock airframes.
