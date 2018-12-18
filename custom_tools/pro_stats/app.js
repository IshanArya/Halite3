const request = require('request-promise-native');

let games = [];

const USER_URI = (user, limit, current) => `https://api.2018.halite.io/v1/api/user/${user}/match?order_by=desc,time_played&limit=${limit}&offset=${current}`;
const shipyardValues = {
    2: {
        32: 8,
        40: 11,
        48: 12,
        56: 14,
        64: 16
    },
    4: {
        32: 8,
        40: 11,
        48: 14,
        56: 18,
        64: 21
    }
}

const minimumDistanceFromShipyard = {
    2: {
        32: 1000,
        40: 1000,
        48: 1000,
        56: 1000,
        64: 1000
    },
    4: {
        32: 1000,
        40: 1000,
        48: 1000,
        56: 1000,
        64: 1000
    }
}

function getManhattanDistance(mapWidth, source, dest) {
    let actualDistance = {
        x: Math.abs(parseInt(dest.x) - parseInt(source.x)),
        y: Math.abs(parseInt(dest.y) - parseInt(source.y))
    };

    mapWidth = parseInt(mapWidth);

    return new Promise((resolve, reject) => resolve(Math.min(actualDistance.x, mapWidth - actualDistance.x) + 
        Math.min(actualDistance.y, mapWidth - actualDistance.y)));
}
function arePositionsEqual(a, b) {
    if(a.x != b.x) {
        return false;
    }
    if(a.y != b.y) {
        return false;
    }
    return true;
}

function getShipyardPosition(game, data) {
    let playerIndex = game.players[data.user].player_index;

    let numberOfPlayers = game.stats.player_statistics.length;
    let mapHeight = game.map_height;
    let shipyardPosition = {};
    if (playerIndex == 0 || playerIndex == 3) {
        shipyardPosition.x = shipyardValues[numberOfPlayers][mapHeight];
    } else {
        shipyardPosition.x = mapHeight - 1 - shipyardValues[numberOfPlayers][mapHeight];
    }
    if (numberOfPlayers == 2) {
        shipyardPosition.y = mapHeight / 2;
    } else {
        if (playerIndex == 0 || playerIndex == 1) {
            shipyardPosition.y = shipyardValues[numberOfPlayers][mapHeight];
        } else {
            shipyardPosition.y = mapHeight - 1 - shipyardValues[numberOfPlayers][mapHeight];
        }
    }
    return new Promise((resolve, reject) => resolve(shipyardPosition));
}
function getDropoffs(game, data) {
    let playerIndex = game.players[data.user].player_index;
    let playerStatistics = game.stats.player_statistics[playerIndex];

    return new Promise((resolve, reject) => resolve(playerStatistics.halite_per_dropoff));
}
function getDropoffPositions(game, data) {
    return getDropoffs(game, data).then(dropoffs => {
        let dropoffPositions = [];
        dropoffs.forEach(e => {
            dropoffPositions.push(e[0]);
        });

        return new Promise((resolve, reject) => resolve(dropoffPositions));
    });
}

function getGameLinks(user, limit) {
    const MAX_RESULTS = 250;
    let current = 0;
    let links = [];

    while (current < limit) {
        let current_limit = limit - current >= MAX_RESULTS ? MAX_RESULTS : limit - current;
        links.push(USER_URI(user, current_limit, current));
        current += MAX_RESULTS;
    }
    return new Promise((resolve, reject) => resolve({
        links: links,
        limit: limit,
        user: user
    }));
}

function parseGameJson(data) {
    for(let i = 0; i < data.links.length; i++) {
        return request(data.links[i]).then(body => {
            let gameInfo = JSON.parse(body);
            games = games.concat(gameInfo);
            if (games.length == data.limit) {
                return data;
            } else {
                throw new Error(`Games Array Length: ${games.length}`);
            }
        }).catch(err => {
            console.error("Caught error!");
            console.error(err.message);
        });
    }
}

async function doStuffWithInfo(data) {
    let avgDistance = 0;
    let totalDropoffs = 0;
    console.log(data.user);
    for(let i = 0; i < games.length; i++) {
        let game = games[i];
        let numberOfPlayers = game.stats.player_statistics.length;
        let mapHeight = game.map_height;
        await getShipyardPosition(game, data).then(async (shipyardPosition) => {
            console.log(`Game ${game.game_id}, Player ${data.user} shipyard position: (${shipyardPosition.x}, ${shipyardPosition.y})`);
            console.log(`Game Width: ${mapHeight}`);
            await getDropoffPositions(game, data).then(async dropoffPositions => {
                let totalDistance = 0;
                await dropoffPositions.forEach(async (e, i) => {
                    if(!arePositionsEqual(e, shipyardPosition)) {
                        console.log(`\tDropoff ${i} @ (${e.x}, ${e.y})`);
                        await getManhattanDistance(mapHeight, shipyardPosition, e).then(distance => {
                            if(minimumDistanceFromShipyard[numberOfPlayers][mapHeight] > distance) {
                                minimumDistanceFromShipyard[numberOfPlayers][mapHeight] = distance;
                            }
                            totalDistance += distance;
                        });
                    }
                });
                console.log(`\tTotal Dropoff Distance: ${totalDistance}`);
                let averageDistance = totalDistance / (dropoffPositions.length - 1);
                console.log(`\tAverage Dropoff Distance: ${averageDistance}`);
            })
        });
        
    }
    return minimumDistanceFromShipyard;
}

getGameLinks(2807, 250).then(parseGameJson).then(doStuffWithInfo).then(distances => {
    console.log("Minimum Distances From Shipyard");
    console.log(`\t2`);
    console.log(`\t\t32:${minimumDistanceFromShipyard[2][32]}`);
    console.log(`\t\t40:${minimumDistanceFromShipyard[2][40]}`);
    console.log(`\t\t48:${minimumDistanceFromShipyard[2][48]}`);
    console.log(`\t\t56:${minimumDistanceFromShipyard[2][56]}`);
    console.log(`\t\t64:${minimumDistanceFromShipyard[2][64]}`);
    console.log(`\t4`);
    console.log(`\t\t32:${minimumDistanceFromShipyard[4][32]}`);
    console.log(`\t\t40:${minimumDistanceFromShipyard[4][40]}`);
    console.log(`\t\t48:${minimumDistanceFromShipyard[4][48]}`);
    console.log(`\t\t56:${minimumDistanceFromShipyard[4][56]}`);
    console.log(`\t\t64:${minimumDistanceFromShipyard[4][64]}`);
});
