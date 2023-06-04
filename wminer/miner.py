

import argparse
import socket
import select
import binascii

import pyrx
import struct
import json
import sys
import os
import time
from multiprocessing import Process, Queue



pool_host = 'gulf.moneroocean.stream'
pool_port = 10002
gpool_pass = 'cozmonot'
wallet_address = '49FrBm432j9fg33N8PrwSiSig7aTrxZ1wY4eELssmkmeESaYzk2fPkvfN7Kj4NHMfH11NuhUAcKc5DkP7jZQTvVGUnD243g'
nicehash = False



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
q = Queue()
pool_ip = socket.gethostbyname(pool_host)
s.connect((pool_ip, pool_port))

global hhunx  

hhunx =-1



def controller(q,s,t,k):
    
    
    try:
    
    
    

        login = {
            'method': 'login',
            'params': {
                'login': wallet_address,
                'pass': gpool_pass + str(t),
                'rigid': '',
                'agent': 'stratum-miner-py/0.1'
            },
            'id':1
        }
        print('Logging into pool: {}:{}'.format(pool_host, pool_port))
        print('Using NiceHash mode: {}'.format(nicehash))
        s.sendall(str(json.dumps(login)+'\n').encode('utf-8'))

        wo = Process(target=worker, args=(q, s))
        wo.daemon = True
        wo.start()
    

        try:
            while 1:
                line = s.makefile().readline()
                r = json.loads(line)
            
                error = r.get('error')
                result = r.get('result')
                method = r.get('method')
                params = r.get('params')
                if error:
                    print('Error: {}'.format(error))
                
                    continue
                if result and result.get('status'):
                    print('Status: {}'.format(result.get('status')))
                
                    k  +=1

                if result and result.get('job'):
                    login_id = result.get('id')
                    job = result.get('job')
                    job['login_id'] = login_id
                    q.put(job)
                elif method and method == 'job' and len(login_id):
                    q.put(params)

        except KeyboardInterrupt:
            print('{}Exiting'.format(os.linesep))
            wo.terminate()
            s.close()
            sys.exit(0)

    except:
        controller(q,s,t,k)



def worker(q, s):
    try:
        started = time.time()
        hash_count = 0

        while 1:
            job = q.get()
        
            login_id = job.get('id')
            print('Login ID: {}'.format(login_id))

            blob = job.get('blob')
            target = job.get('target')
            job_id = job.get('job_id')
            height = job.get('height')
            block_major = int(blob[:2], 16)
            cnv = 0
            if block_major >= 7:
                cnv = block_major - 6
            if cnv > 5:
                seed_hash = binascii.unhexlify(job.get('seed_hash'))
                print('New job with target: {}, RandomX, height: {}'.format(target, height))
            else:
                print('New job with target: {}, CNv{}, height: {}'.format(target, cnv, height))
            xntarget = struct.unpack('I', binascii.unhexlify(target))[0]
            target = struct.unpack('I', binascii.unhexlify(target))[0]
            if target >> 32 == 0:
                target = int(0xFFFFFFFFFFFFFFFF / int(0xFFFFFFFF / target))
            nonce = 1

            xbin = binascii.unhexlify(blob)
            print(len(blob))
            fbin = struct.pack('39B', *bytearray(xbin[:39]))
            lbin = struct.pack('{}B'.format(len(xbin)-43), *bytearray(xbin[43:]))

            while 1:
            
            
            
                hash = pyrx.get_rx_hash(fbin,lbin, seed_hash, height,target,nonce)
           
            
                np = open("non.txt", "r")
                nonce = int(np.read())
            
                sys.stdout.flush()
                hex_hash = binascii.hexlify(hash).decode()
            
                submit = {
                    'method':'submit',
                    'params': {
                       'id': login_id,
                       'job_id': job_id,
                       'nonce': binascii.hexlify(struct.pack('<I', nonce)).decode(),
                    'result': hex_hash
                    },
                    'id':1
                }
                print('Submitting hash: {}'.format(hex_hash))
            
            
                s.sendall(str(json.dumps(submit)+'\n').encode('utf-8'))
                select.select([s], [], [], 3)
            
                np.close()
                np = open("non.txt", "w")
                np.truncate(0)
                np.close()
         
                if not q.empty():    
                    break
    except:
        worker(q,s)
                
            

if __name__ == '__main__':

    

    parser = argparse.ArgumentParser()
    parser.add_argument('--nicehash', action='store_true', help='NiceHash mode')
    parser.add_argument('--host', action='store', help='Pool host')
    parser.add_argument('--port', action='store', help='Pool port')
    args = parser.parse_args()
    if args.nicehash:
        nicehash = True
    if args.host:
        pool_host = args.host
    if args.port:
        pool_port = int(args.port)

    controller(q, s,1,hhunx)
