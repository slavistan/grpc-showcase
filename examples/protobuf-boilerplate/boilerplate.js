// CommonJS imports breaks intellisense :( See
// https://stackoverflow.com/questions/64565836/how-to-setup-vscode-intellisense-for-protobuf-generated-javascript-files
const Schema = require('./proto-out/boilerplate_pb.js')

// Create message
const batch = new Schema.HourlySensorBatch()
batch.setSensorid(4493)
batch.setMeasurementsList([144, 145, 146, 146, 148, 148, 149, 150])
batch.addCoords(88.45);
batch.addCoords(44.93);
batch.setHod(16)

// Convert object from message
const batch_obj = batch.toObject()
console.log(batch_obj)

// Serialize message
// msg.setSensorid("Peter Müller") // lazy type checking
const batch_bin = batch.serializeBinary()
console.log(`Message size: ${batch_bin.length}`)
console.log(`JSON size: ${JSON.stringify(batch_obj).length}`)

// Create nested message
const log = new Schema.LogMessage()
log.setData(batch)
log.setComment('Alarm! Alarm!')

// Serialize and print length
const log_bin = log.serializeBinary()