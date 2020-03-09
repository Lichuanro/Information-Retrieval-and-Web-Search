import pickle as pkl
from .query import Query
from .document import Document
import math

class NDCG:
    def get_rel_scores(self, filename):
        self.rel_scores = {}
        query = ""
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith("q"):
                    query = line.split(":")[-1].strip()
                    url_score = {}
                    self.rel_scores[query] = url_score
                else: #urls
                    tokens = line[line.index(":")+1:].strip().split(" ")
                    url = tokens[0]
                    rel = tokens[1]
                    if float(rel) < 0:
                        rel = 0
                    if url_score is not None:
                        url_score[url] = float(rel)

    def calc_ndcg(self, rels):
        local_sum = 0
        sorted_sum = 0
        for i in range(len(rels)):
            rel = rels[i]
            local_sum += (2**rel - 1) / (math.log(i + 1 + 1, 2))
        sorted_rels = sorted(rels, reverse=True)
        for i in range(len(sorted_rels)):
            rel = sorted_rels[i]
            sorted_sum += (2**rel - 1) / (math.log(i + 1 + 1, 2))

        if (sorted_sum == 0):
            return 0
        else:
            return local_sum/sorted_sum

    def read_ranking_calc(self, ranked_result_file):
        self.query_ndcg = {}
        self.query_docs = {}
        cur_q = ""
        cur_rels = []

        with open(ranked_result_file, 'r') as f:
            for line in f:
                clean_l = line.strip().split(":")
                l_type = clean_l[0].strip()
                l_content = ":".join(clean_l[1:]).strip()
                if l_type == 'query':
                    if len(cur_rels) > 0:
                        self.query_ndcg[cur_q] = self.calc_ndcg(cur_rels)
                    cur_q = l_content
                    cur_rels = []
                    self.query_docs[cur_q] = []
                elif l_type == 'url':
                    doc = Document(l_content)
                    self.query_docs[cur_q].append(doc)
                    if (cur_q in self.rel_scores) and \
                       (doc.url in self.rel_scores[cur_q]):
                        cur_rels.append(self.rel_scores[cur_q][doc.url])
                    else:
                        print("Warning. Cannot find query %s with url %s"%(cur_q, doc.url))
                elif l_type == 'title':
                    doc.title = l_content
                # ignore debug line for now

        if len(cur_rels) > 0:
            self.query_ndcg[cur_q] = self.calc_ndcg(cur_rels)
            cur_q = l_content
            cur_rels = []

    def get_avg_ndcg(self):
        sum_ndcg = 0
        for i in self.query_ndcg:
            sum_ndcg += self.query_ndcg[i]
        return sum_ndcg / len(self.query_ndcg)

    def write_ndcg_result(self, ndcg_result_file):
        with open(ndcg_result_file, 'w') as f:
            for query in self.query_ndcg:
                f.write("query: " + query + "\n")
                ndcg_score = self.query_ndcg[query]
                f.write("ndcg: " + str(ndcg_score) + "\n")

                for doc in self.query_docs[query]:
                    f.write("  url: " + doc.url + "\n")
                    f.write("    rating: " + str(self.rel_scores[query][doc.url]) + "\n")
                    f.write("    title: " + doc.title + "\n")
                    f.write("    debug:" + "\n")

        print("Write ndcg result to " + ndcg_result_file + " sucessfully!")
