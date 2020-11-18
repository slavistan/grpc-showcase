# gRPC

**Artikel**

 - https://nordicapis.com/when-to-use-what-rest-graphql-webhooks-grpc/
 - https://github.com/grpc-ecosystem/awesome-grpc

> RPC is a method for executing a procedure on a remote server, somewhat akin to running a program on a friend’s computer miles from your workstation
> Whereas REST defines its interactions through terms standardized in its requests, RPC functions upon an idea of contracts, [...]
> RPC gives much of the power (and responsibility) to the client for execution, while offloading much of the handling and computation to the remote server hosting the resource

## Aspekte

Protobuf/gRPC validiert In-/Output-Datenformate. Ungültige Eingaben werden am Client abgefangen.
Vgl. Json or XML, welche keine Datenprüfung haben und als "Strings" versandt werden.

"Backend-to-backend" Kommunikation

GRPC verwendet "Services" welche mittels "Messages" kommunizieren

Stubs definieren die low-level Kommunikationsdetails und werden automatisch definiert.

Protobuf Kodierung: Viel Bitgeschubse; sehr effiziente Operationen

Behandeln:

- Generierter, sprachenspezifischer Code https://developers.google.com/protocol-buffers/docs/reference/overview
- Message vs. MessageLite --> Für lightweight Umgebung
- Sonstiges Tooling (Json-Konversion, Debugging, ...)
- JSON/HTTP1.1 vs. Protobuf/HTTP2 Speedtest
- Java-Script: JSON in Objekt einlesen vs. Protobuf decoden --> Fast Json referenz
- gRPC im Browser: https://grpc.io/blog/state-of-grpc-web/ -> Bisher nur Backend-to-Backend
- Protobuf komprimiert numerische Daten gut, HTTP2 (Huffman-Encoding) übernimmt Datenworte

### Why not REST?

REST verbs (GET, POST, PUT, DELETE, ...) map very well to CRUD operations against a resource. Once different kinds
of operations are required the simplicity and expressiveness of the used constructs diminishes (PATCH, PUT, POST) whence
it becomes evident that REST is a convention-based way of communication.
