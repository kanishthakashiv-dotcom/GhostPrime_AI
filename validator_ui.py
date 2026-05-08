import streamlit as st
from ghost_engine import GhostEngine
from test_suite import GhostTestSuite
from Bio import SeqIO
import io

st.set_page_config(page_title="GhostPrime AI", page_icon="👻", layout="wide")

st.title("👻 GhostPrime AI: Universal PCR Auditor")
st.markdown("---")

# --- SIDEBAR ---
st.sidebar.header("Step 1: Choose Mode")
mode = st.sidebar.selectbox("Analysis Type", ["Custom Upload", "pandemic", "guardian", "auditor"])

target_seq = None
ghost_seq = None
default_fwd = ""
default_rev = ""

if mode == "Custom Upload":
    st.sidebar.subheader("Upload FASTA Files")
    # FIXED THE COMMAND BELOW:
    target_file = st.sidebar.file_uploader("Upload Target Genome (Signal)", type=["fasta", "fna"], key="target")
    ghost_file = st.sidebar.file_uploader("Upload Ghost Genome (Noise/Host)", type=["fasta", "fna"], key="ghost")
    
    if target_file and ghost_file:
        # Read from uploaded buffer
        target_seq = next(SeqIO.parse(io.StringIO(target_file.getvalue().decode("utf-8")), "fasta")).seq
        ghost_seq = next(SeqIO.parse(io.StringIO(ghost_file.getvalue().decode("utf-8")), "fasta")).seq
else:
    # Use existing local files from SHORT_PROJECT
    config = GhostTestSuite.get_data_config(mode)
    ready, missing_file = GhostTestSuite.verify_files(config)
    if ready:
        target_seq = SeqIO.read(config['target_file'], "fasta").seq
        ghost_seq = SeqIO.read(config['ghost_file'], "fasta").seq
        default_fwd, default_rev = config['primers']
    else:
        st.error(f"Missing local file: {missing_file}")

# --- MAIN INTERFACE ---
if target_seq and ghost_seq:
    st.header("Step 2: Define Primers")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        f_input = st.text_input("Forward Primer (5'-3')", default_fwd)
    with col_p2:
        r_input = st.text_input("Reverse Primer (5'-3')", default_rev)

    if st.button("🚀 Run Universal Ghost Audit"):
        target_eng = GhostEngine(target_seq)
        ghost_eng = GhostEngine(ghost_seq)
        
        # Thermodynamics
        f_stats = target_eng.get_thermodynamics(f_input)
        r_stats = target_eng.get_thermodynamics(r_input)
        
        st.subheader("📊 Primer Properties")
        st.write(f"**Forward Tm:** {f_stats['tm']}°C | **Reverse Tm:** {r_stats['tm']}°C")

        # Logic
        with st.spinner("Scanning for Ghost interference..."):
            f_ghosts = ghost_eng.find_potential_hits(f_input)
            r_ghosts = ghost_eng.find_potential_hits(r_input)

        # Final Verdict
        if len(f_ghosts) + len(r_ghosts) > 0:
            st.error(f"❌ CRITICAL ALERT: {len(f_ghosts) + len(r_ghosts)} Ghost hits found in the background genome!")
            st.expander("Show Ghost Locations").write({"Forward": f_ghosts, "Reverse": r_ghosts})
        else:
            st.success("✅ OPTIMIZED: Primers are specific and show no background interference.")
else:
    st.info("Please select a scenario or upload your own FASTA files in the sidebar to begin.")
