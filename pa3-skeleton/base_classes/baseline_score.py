class BaselineScorer(AScorer):
    def __init__(self, idf):
        super().__init__(idf)
    
    def get_sim_score(self, q, d):
        q_vec = self.get_query_vector(q)
        d_vec = self.get_doc_vector(q, d)
        score = 0
        if 'body_hits' in d_vec.keys():
            for term in d_vec['body_hits'].keys():
                score += d_vec['body_hits'][term]
        return score