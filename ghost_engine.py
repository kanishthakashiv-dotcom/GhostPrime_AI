import math
from Bio.SeqUtils import MeltingTemp as mt
from Bio.Seq import Seq

class GhostEngine:
    def __init__(self, reference_seq):
        self.reference = str(reference_seq).upper()

    def get_thermodynamics(self, primer_seq):
        primer_obj = Seq(primer_seq)
        tm = mt.Tm_NN(primer_obj)
        gc_content = (primer_seq.count('G') + primer_seq.count('C')) / len(primer_seq) * 100
        return {"tm": round(tm, 2), "gc": round(gc_content, 2)}

    def weighted_score(self, primer, target_segment):
        """Weights the 3' end (last 5 bases) 10x more than the rest."""
        if len(primer) != len(target_segment):
            return 0
        score, total_weight = 0, 0
        weights = [1] * (len(primer) - 5) + [10] * 5 
        for p, t, w in zip(primer, target_segment, weights):
            total_weight += w
            if p == t: score += w
        return score / total_weight

    def find_potential_hits(self, primer, threshold=0.75):
        primer = primer.upper()
        p_len = len(primer)
        hits = []
        # Search Forward and Reverse Complement
        strands = [primer, str(Seq(primer).reverse_complement())]
        for p_seq in strands:
            for i in range(len(self.reference) - p_len):
                window = self.reference[i:i+p_len]
                score = self.weighted_score(p_seq, window)
                if score >= threshold:
                    hits.append({"position": i, "score": round(score, 2), "sequence": window})
        return hits
