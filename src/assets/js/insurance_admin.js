document.addEventListener("DOMContentLoaded",function(){

const manager = document.getElementById("id_manager");

manager.addEventListener("change",filter_subs);


const province = document.getElementById("id_origin_province");

province.addEventListener("change",filter_county);



function filter_subs(){
  const subsets = document.getElementById('id_subsets');
  $.ajax({
                    url: "/insurance/ajax/sub_users",
                    type:"GET",
                    data: {"manager_id":manager.value},
                    success: function (result) {
                        subsets.innerHTML = "";
                         result.forEach(element => {
                          debugger;
                          let opt = document.createElement("option");
                          opt.innerHTML = element.national_code;
                          opt.value = element.id;

                          subsets.appendChild(opt);
                          
                        });
                    }
                });
}


function filter_county(){
  const county = document.getElementById("id_origin_county");

    $.ajax({
                    url: "/insurance/get_counties/",
                    type:"GET",
                    data: {"province_id":province.value},
                    success: function (result) {
                      county.innerHTML = "";
                      result.forEach(element=> {
                        let opt = document.createElement("option");
                        opt.value = element.id;
                        opt.innerHTML = element.name;
                        county.appendChild(opt);

                      })
                    }
    })

}


});
