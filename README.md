# Campaigns
## /campaigns/
GET
```json
[
    {
        "id": <id>,
        "name": <string name>,
        "gm": <string user>,
        "created": <datetime>,
        "updated": <datetime>,
        "players": [
            {
                "id": <id>,
                "name": <string>,
                "character_name": <string>,
                "email": <string>
            }...
        ]
    }...
]
```

POST
```json
{
    "name": <string name>,
    "gm": <string user>
}
```

## /campaigns/##
GET
```json
{
    "id": <string uuid>,
    "name": <string name>,
    "gm": <string user>,
    "created": <datetime>,
    "updated": <datetime>,
    "players": [
        {
            "id": <id>,
            "name": <string>,
            "character_name": <string>,
            "email": <string>,
            "created": <datetime>,
            "updated": <datetime>
        }..
    ]
}
```

POST
```json
{
    "name": <string name>,
    "gm": <string user>
}
```

DELETE

## /campaigns/##/sessions
GET
```json
[
    {
        "id": <id>,
        "name": <string name>,
        "created": <datetime>
    }...
]
```

POST
```json
{
    "name": <string name>,
    "created": <datetime>
}
```

## /campaigns/##/sessions/##
GET
```json
{
    "id": <id>,
    "name": <string name>,
    "created": <datetime>
}
```

POST
```json
{
    "name": <string name>
}
```

DELETE

## /campaigns/##/encounters
GET
```json
[
    {
        "id": <id>,
        "name": <string name>,
        "created": <datetime>,
        "updated": <datetime>
    }...
]
```

POST
```json
{
    "name": <string name>
}
```

## /campaigns/##/encounters/##
GET
```json
{
    "id": <id>,
    "name": <string name>,
    "created": <datetime>,
    "updated": <datetime>
}
```

POST
```json
{
    "name": <string name>
}
```

DELETE

## /campaigns/##/encounters/##/items
GET
```json
[
    {
        "id": <id>,
        "name": <string>,
        "type": <string>,
        "price": <float>,
        "quantity": <int>,
        "sale_percent": <float>,
        "weight": <float>,
        "created": <datetime>,
        "updated": <datetime>
    }...
]
```

POST
```json
{
    "name": <string>,
    "type": <string>,
    "price": <float>,
    "quantity": <int>,
    "sale_percent": <float>,
    "weight": <float>,
}
```

## /campaigns/##/encounters/##/items/##
GET
```json
{
    "id": <id>,
    "name": <string>,
    "type": <string>,
    "price": <float>,
    "quantity": <int>,
    "sale_percent": <float>,
    "weight": <float>,
    "created": <datetime>,
    "updated": <datetime>
}
```

POST
```json
{
    "name": <string>,
    "type": <string>,
    "price": <float>,
    "quantity": <int>,
    "sale_percent": <float>,
    "weight": <float>
}
```

DELETE

## /campaigns/##/players
GET
```json
[
    {
        "id": <id>,
        "name": <string>,
        "character_name": <string>,
        "email": <string>,
        "created": <datetime>,
        "updated": <datetime>
    }...
]
```

POST
```json
{
    "name": <string>,
    "character_name": <string>,
    "email": <string>
}
```

## /campaigns/##/players/##
GET
```json
{
    "id": <id>,
    "name": <string>,
    "character_name": <string>,
    "email": <string>,
    "created": <datetime>,
    "updated": <datetime>
}
```

POST
```json
{
    "name": <string>,
    "character_name": <string>,
    "email": <string>
}
```

DELETE

## /campaigns/##/players/##/loot
see */loot

## /campaigns/##/players/##/loot/##
see */loot/##


## /campaigns/##/loot
see */loot

## /campaigns/##/loot/##
see */loot/##

## *#/loot
GET
```json
[
    {
        "id": <id>,
        "name": <string>,
        "type": <string>,
        "price": <float>,
        "quantity": <int>,
        "sale_percent": <float>,
        "weight": <float>,
        "owner": <string, player name or null>,
        "created": <datetime>,
        "updated": <datetime>,
        "transactions": [
            {
                "id": <id>,
                "session_id": <id>,
                "owner": <string>,
                "notes": <string>,
                "created": <datetime>,
                "updated": <datetime>
            }
        ]
    }...
]
```

POST
```json
{
    "name": <string>,
    "type": <string>,
    "price": <float>,
    "quantity": <int>,
    "sale_percent": <float>,
    "weight": <float>
}
```

## */loot/##
GET
```json
{
    "id": <id>,
    "name": <string>,
    "type": <string>,
    "quantity": <int>,
    "price": <float>,
    "sale_percent": <float>,
    "weight": <float>,
    "owner": <string, player name or null>,
    "created": <datetime>,
    "updated": <datetime>,
    "transactions": [
        {
            "id": <id>,
            "session_id": <id>,
            "owner": <string>,
            "notes": <string>,
            "price": <float>,
            "created": <datetime>,
            "updated": <datetime>
        }
    ]
}...
```

POST
```json
{
    "name": <string>,
    "type": <string>,
    "price": <float>,
    "quantity": <int>,
    "sale_percent": <float>,
    "weight": <float>,
    "owner": <string, player name or null>
}...
```

DELETE

## */loot/##/transactions
GET
```json
[
    {
        "id": <id>,
        "session_id": <id>,
        "owner": <string>,
        "notes": <string>
        "created": <datetime>,
        "updated": <datetime>
    }
]
```

POST

## */loot/##/transactions/##
GET
```json
{
    "id": <id>,
    "session_id": <id>,
    "owner": <string>,
    "notes": <string>,
    "created": <datetime>,
    "updated": <datetime>
}
```

POST
```json
{
    "session_id": <id>,
    "owner": <string>,
    "notes": <string>
}
```

DELETE

