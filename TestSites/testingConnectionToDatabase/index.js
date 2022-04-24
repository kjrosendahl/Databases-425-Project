// npm install oracledb
// Documentation Link: https://oracle.github.io/node-oracledb/doc/api.html
const oracledb = require('oracledb');

function test() {

    let connection;

    connection = oracledb.getConnection({
        user: "noah",
        password: "noah",
        connectString: "localhost/xepdb1"
    }).then( (connection) => {

        console.log("Connected to database 'xepdb1' with user 'noah'");
        
        connection.execute(
            `SELECT *
            FROM course
            WHERE credits = 4`
        ).then( (result) => {
            console.log(result.rows);
            connection.close();
        }).catch( (err) => {
            console.log(`Selection Error: ${err}`);
            console.log('Closing Connection');
            connection.close();
        })

    }).catch( (err) => {
        console.log(`Error: ${err}`);
        console.log('Closing Connection');
        connection.close();
    });

}

test()

