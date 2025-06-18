{

  "type": "Request",

  "kind": "Skills",

  "inputs": {

    "schema": {

    "type": "object",

    "properties": {

    "text": {

    "description": "Please enter your input",

    "title": "SearhQuery",

    "type": "string",

    "x-ms-content-hint": "TEXT",

    "x-ms-dynamically-added": true

    }

    },

    "required": [

    "text"

    ]

    }

  },

  "metadata": {

    "operationMetadataId": "f0d2a9ff-4ac5-47cc-b95b-42e03b5a1e19"

  }

}



{

  "type": "OpenApiConnection",

  "inputs": {

    "parameters": {

    "dataset": "https://1c5m1h.sharepoint.com",

    "table": "dd6cb496-8394-4c38-8e24-28c9769fb905",

    "$filter": "substringof('@{triggerBody()['text']}', FileLeafRef)",

    "$top": 5,

    "viewScopeOption": "RecursiveAll"

    },

    "host": {

    "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",

    "connection": "shared_sharepointonline-2",

    "operationId": "GetFileItems"

    }

  },

  "runAfter": {},

  "metadata": {

    "operationMetadataId": "ec28d87d-267e-4162-9493-5602714e1672"

  }

}



{

  "type": "Foreach",

  "foreach": "@outputs('Get_files_(properties_only)')?['body/value']",

  "actions": {

    "Parse_JSON": {

    "type": "ParseJson",

    "inputs": {

    "content": "@outputs('Get_files_(properties_only)')?['body/value']",

    "schema": {

    "type": "array",

    "items": {

    "type": "object",

    "properties": {

    "@@search.score": {

    "type": "number"

    },

    "name": {

    "type": "string"

    },

    "ServerRedirectedURL": {

    "type": "string"

    },

    "LastModifiedTime": {

    "type": "string"

    },

    "FileType": {

    "type": "string"

    }

    }

    }

    }

    },

    "metadata": {

    "operationMetadataId": "bac473ee-b918-492b-a5f1-c887da63cd97"

    }

    }

  },

  "runAfter": {

    "Get_files_(properties_only)": [

    "Succeeded"

    ]

  },

  "metadata": {

    "operationMetadataId": "cdf8f24e-4b6d-4a63-a71d-09227c2a35f0"

  }

}



{

  "type": "ParseJson",

  "inputs": {

    "content": "@outputs('Get_files_(properties_only)')?['body/value']",

    "schema": {

    "type": "array",

    "items": {

    "type": "object",

    "properties": {

    "@@search.score": {

    "type": "number"

    },

    "name": {

    "type": "string"

    },

    "ServerRedirectedURL": {

    "type": "string"

    },

    "LastModifiedTime": {

    "type": "string"

    },

    "FileType": {

    "type": "string"

    }

    }

    }

    }

  },

  "metadata": {

    "operationMetadataId": "bac473ee-b918-492b-a5f1-c887da63cd97"

  }

}



{

  "type": "Response",

  "kind": "Skills",

  "inputs": {

    "schema": {

    "type": "object",

    "properties": {

    "fileresults": {

    "title": "FileResults",

    "x-ms-dynamically-added": true,

    "type": "string"

    }

    },

    "additionalProperties": {}

    },

    "statusCode": 200,

    "body": {

    "fileresults": "@{outputs('Get_files_(properties_only)')?['body/value']}"

    }

  },

  "runAfter": {

    "For_each": [

    "Succeeded"

    ]

  },

  "metadata": {

    "operationMetadataId": "34cdb1b3-f384-4edd-bf70-486836704d55"

  }

}
