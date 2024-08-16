### **get_block_count**

Look up how many blocks are in the longest chain known to the node.

Alias: *getblockcount*.

Inputs: *None*.

Outputs:

* *count* - unsigned int; Number of blocks in longest chain seen by the node.
* *status* - string; General RPC error code. "OK" means everything looks good.
* *untrusted* - boolean; States if the result is obtained using the bootstrap mode, and is therefore not trusted (`true`), or when the daemon is fully synced and thus handles the RPC locally (`false`)

Example:

```
$ curl http://127.0.0.1:18081/json_rpc -d '{"jsonrpc":"2.0","id":"0","method":"get_block_count"}' -H 'Content-Type: application/json'  

{  
  "id": "0",  
  "jsonrpc": "2.0",  
  "result": {  
    "count": 993163,  
    "status": "OK"
    "untrusted": "false"  
  }  
}  
```


### **on_get_block_hash**

Look up a block's hash by its height.

Alias: *on_getblockhash*.

Inputs:

* block height (int array of length 1)

Outputs:

* block hash (string)

Example:

```
$ curl http://127.0.0.1:18081/json_rpc -d '{"jsonrpc":"2.0","id":"0","method":"on_get_block_hash","params":[912345]}' -H 'Content-Type: application/json'

{
  "id": "0",
  "jsonrpc": "2.0",
  "result": "e22cf75f39ae720e8b71b3d120a5ac03f0db50bba6379e2850975b4859190bc6"
}
```
