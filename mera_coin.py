# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import datetime
import hashlib
import json
from flask import Flask,jsonify,request
import requests
from uuid import uuid4
from urllib.parse import urlparse

 
# Building  a blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.transactions=[]
        self.create_block(proof=1, previous_hash = '0')# this is the geneisis block so previous_has==h =0
        self.nodes=set()
        
    def create_block(self,proof,previous_hash):
        block={
                'index':len(self.chain)+1,
                'timestamp':str(datetime.datetime.now()),
                'proof':proof,
                'previous_hash':previous_hash,
                'transactions':self.transactions
                } 
        self.transactions=[]
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    #proof_of_work function is for the miners to solve the puzzle 
    def proof_of_work(self,previous_proof):
        new_proof=1
        check_proof=False #to check while this is false
        while check_proof is False:
            hash_operation=hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest() 
            ## new_proof^2-previous^proof b/c if it was new_proof+prev_proof it 
            #would repeat when previos_proof becomes new_proof 
            #and not new-prev just to increase the complexity
            if hash_operation[:4]== '0000':
                check_proof=True
            else:
                new_proof+=1
        return new_proof
    
    def hash(self,block):
        encoded_block= json.dumps(block,sort_keys=True).encode()# converts the block into a json sort_key sorts acc to key pf dict
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block=chain[0]
        block_index=1
        while block_index<len(chain):
            block=chain[block_index]
            if block['previous_hash']!=self.hash(previous_block):
                return False
            previous_proof=previous_block['proof']
            proof=block['proof']
            hash_operation=hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest() 
            if hash_operation[:4]!= '0000':
                return False
            previous_block=block
            block_index+=1
            
        return True
    def add_transaction(self,sender,receiver,amount):
        self.transaction.append({'sender':sender,
                                 'receiver':receiver,
                                 'amount':amount})
        previous_block=self.get_previous_block()
        return previous_block['index']+1
    
    def add_node(self,address):
        parsed_url=urlparse(address)
        self.nodes.add(parsed_url.netloc) #if address is http:/127.0.0:5000/ .netloc gives 127.0.0:5000
    
    def replace_chain(self):
        network=self.nodes
        longest_chain=None
        max_length=len(self.chain)
        for node in network:
            response=requests.get(f'http:/{node}/get_chain')
            length=response.json()['length']
            chain=response.jsoon()['chain']
            if length>max_length and self.is_chain_valid(chain):
                max_length=length
                longest_chain=chain
        if longest_chain: #if longest_chain is not None
            self.chain=longest_chain
            return True
        return False
        
            
# mining a block

# create a web app
app=Flask(__name__)

 #Creating a address for the node onport 5000
 node_address=str(uuid4()).replace('-','')

#create a blockchain
blockchain=Blockchain()            
print (len(blockchain.chain))
#mine a new block
@app.route('/mine_block',methods=['GET'])
def mine_block():
    previous_block=blockchain.get_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address,recevier='Kaustubh',amount=101)
    block=blockchain.create_block(proof,previous_hash)
    response={'message':'Wahah Waha bana diya block',
              'index':block['index'],
              'timestamp':block['timestamp'],
              'proof':block['proof'],
              'previous_hash':block['previous_hash'],
              'transactions:'block['transactions']
            }
    return jsonify(response),200

# display the blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200
# checking if the blockcahin is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    response={'Status':blockchain.is_chain_valid(blockchain.chain)
            }
    return jsonify(response),200

#Adding new transaction to the blockchian
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json=request.get_json()
    transaction_keys=['sender','receiver','amount']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing',400
    index=blockchain.add_transaction(json['sender'],json['receiver'],json['amount'])
    response={'message':f'This transaction will be added to Block{index}'}
    return jsonify(response),201
# Decentralizing the blockchain
#Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json=request.get_json()
    nodes=json.get('node')
    if nodes is None:
        return "No node",400
    for node in nodes:
        blockchain.add_node(node)
    repsonse={'message':'All the nodes are now connected.The blockchain now contains',
              'total_nodes':list(blockchain.nodes)}
     return jsonify(response),201
# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def connect_node():
    is_chain_replaced=blockchain.replace_chain()
    if is_chain_replaced:
        response:{'message':'The nodes had different chains so it got replaced by the longest chain',
                  'new_chain':blockchain.chain}
    else:
        response={'message':'All good.the chain is the largest one',
                  'actual_chain':blockchain.chain}
    return jsonify(response),200
     
# run the app
app.run(host='0.0.0.0',port=5000)
























 