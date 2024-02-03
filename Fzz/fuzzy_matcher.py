import pandas as pd
import numpy as np
import tqdm


import rapidfuzz
from rapidfuzz import process
from rapidfuzz import utils as fuzz_utils
#from deep_translator import GoogleTranslator


class Lead_fuzzymatch:

    def __init__(self, country,   threshold, limit, baseFrame, compareFrame):
        self.country = country
        self.threshold = threshold  # future: varying threshold by country
        self.limit = limit
        self.baseFrame = baseFrame[baseFrame['PARTNER_COUNTRY'] == self.country]
        self.compareFrame = compareFrame[compareFrame['EXACT_COUNTRY'] == self.country]
        self.baseKey = 'ACCOUNT_NAME'
        self.compareKey = 'BRANCH_PRIMARY_NAME'

    # code block where translation is required

    def country_logic(self):
        if self.country in ['CHINA' ,'JAPAN']:
            self.baseFrame['ACCOUNT_NAME_ORIGINAL'] = self.baseFrame['ACCOUNT_NAME']
            #self.baseFrame['ACCOUNT_NAME'] = self.baseFrame['ACCOUNT_NAME']. \
                #apply(lambda x: GoogleTranslator(source='auto', target='en').translate(x))
        else:
            pass

    # code block where translation is not required.
    def fuzzy_merge(self, threshold=30, limit=3, how='left'):
        self.country_logic()
        s_mapping = {x: fuzz_utils.default_process(str(x)) for x in self.compareFrame[self.compareKey]}
        place_holder = ""
        # fuzzy ratio
        m5 = self.baseFrame[self.baseKey].apply(lambda x: process.extract(
            fuzz_utils.default_process(str(x)), s_mapping, limit=3, score_cutoff=60, processor=None,
            scorer=rapidfuzz.fuzz.partial_ratio
        ))

        self.baseFrame['Match_Ratio'] = m5
        self.baseFrame['Match_Ratio'].fillna("('NONE',0,'NONE'),('NONE',0,'NONE'),('NONE',0,'NONE')")

        m6 = self.baseFrame['Match_Ratio'].apply(lambda x: ', '.join(i[2] for i in x))
        self.baseFrame[['Match1_Ratio', 'Match2_Ratio', 'Match3_Ratio' ]] = pd.DataFrame(
            self.baseFrame.Match_Ratio.tolist(),
            index=self.baseFrame.index)

        self.baseFrame['Match1_Ratio'] = self.baseFrame['Match1_Ratio'].apply(
            lambda x: str(x).split(',')[0].strip("('").upper())
        self.baseFrame[['b1', 'b2', 'b3']] = pd.DataFrame(self.baseFrame['Match_Ratio'].tolist(),
                                                          index=self.baseFrame.index)
        # return baseFrame

        self.baseFrame['b1'].fillna("('NONE',0,'NONE')")
        self.baseFrame[['Ratio_Match', 'threshold', 'Ratio_account']] = pd.DataFrame(self.baseFrame['b1'].tolist(),
                                                                                     index=self.baseFrame.index)
        self.baseFrame[['b1_name', 'b1_threshold' ,'b1_name_upper']] = pd.DataFrame(self.baseFrame['b1'].tolist(), index=self.baseFrame.index)
        self.baseFrame[['b2_name', 'b2_threshold' ,'b2_name_upper']] = pd.DataFrame(self.baseFrame['b2'].tolist(), index=self.baseFrame.index)
        self.baseFrame[['b3_name', 'b3_threshold' ,'b3_name_upper']] = pd.DataFrame(self.baseFrame['b3'].tolist(), index=self.baseFrame.index)

        # self.baseFrame['to_match'] = self.baseFrame[['b1_name_upper','b2_name_upper' ,'b3_name_upper']]
        return self.baseFrame

    def call_gpt(self):

        to_match = 'NSB'
        in_match = ['queensbury hospital pvt ltd' ,'nsbm' ,'gforce it distributions']
        g.gpt_chat(system_message="You are a chatbot", \
                   user_message=f"What is the closest match of {to_match}  \
          in {in_match} ")



