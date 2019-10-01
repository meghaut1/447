var mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "",
  database: "callcenter"
});
//con.query("SELECT * FROM event");

con.connect(function(err) {
  if (err) throw err;
  con.query("SELECT * FROM event", function (err, result, fields) {
    if (err) throw err;
    console.log(result);
    con.destroy();
  });
});

//.exit
