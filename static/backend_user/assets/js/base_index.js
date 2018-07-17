
    new Vue({
        delimiters : ['[[', ']]'],
        el: '#wrapper',
        data: {
          message: 'Hello Vue.js!',
          arr_salle:[],
          arr_prod:[],
          arr_historique:[],
          arr_panier:[],
          product:[],
          panier:[],
          arr_formation:[],
          arr_formation_send:[],
          products_buy:[],
          products_buy_1:[],
          trans_formation:[],
          trans_prod:[],
          loading_panier:false,
          loading_trans_formation:false,
          is_panier:false,
          is_panier_trans:false,
          uuid :"",
          uuid_dar:"",
          token:"",
          url_base : "http://127.0.0.1:8000/api/",
          url_base_dar : "http://127.0.0.1:8000/dar/",
          url_token :  "get-token",
          url_getProduct :  "produit",
          url_salle : "salles/dar=",
          url_transaction : "transaction",
          url_historique:"historique/",
          url_panier:"panier/uuid-panier=",
          url_formation:"formation-dar",
          loading : false,
          hide_home:true,
          salleIsLoaded:false,
          prodIsLoaded:false,
          formIsLoaded:false,
          count: 0,
          search:"5",
         },
         
        watch:
        {
            search:function(oldValue,newValue)
                {
             console.log("watcher : oldvalue = ", oldValue ,"newValue", newValue);
         
             this.get_historique(newValue,oldValue);
              }
        },
        methods: {
          get_salle:function(){
            this.url_salle = this.url_base + this.url_salle + this.uuid_dar;

            
            axios.get(this.url_salle)
                .then(response=>{
                    this.loading = true;
                    if (response.status == 200)
                        {   
                            this.arr_salle = response.data
                            this.salleIsLoaded = true
                            
                        }
                })
                .catch(e => {
                    console.log(e);
                })
            
          },
          get_test:function(){
             
            axios.get("http://127.0.0.1:8000/dar/test")
                .then(response=>{
                    this.loading = true;
                    console.log(response);
                this.$nextTick(() => {
                    this.show = true

                    console.log('re-render start')
                    

                    this.$nextTick(() => {
                        this.$refs.home1.innerHTML = response.data;
                        console.log('re-render end')
                    })

                })
                    
                })
                .catch(e => {
                    console.log(e);
                })
            
          },
          //add produit panier
          add_item:function(prod)
            {
              var item = this.products_buy.findIndex(pp => pp.uuid == prod.uuid);
              var item_products = this.product.findIndex(ite => ite["uuid"] == prod.uuid);

              var qte = parseInt(this.product[item_products]["quantity"]);
              if(qte > 0){
  
              if( item  == -1 )
              {
              this.products_buy.push({uuid:prod.uuid,qte:1,nom:prod.nom,prix:prod.price});
              this.panier.push({nom:prod.product,prix:prod.price,qte:1})
              this.count +=1;
              }else{
                  
                  this.products_buy[item].qte += 1;
                  this.panier[item].qte +=1;
              }

              this.product[item_products]["quantity"] = (qte - 1 ).toString();
              
                 }else{
              alert("stock epuisé");
               }

            },
          add_item_formation:function(formation)
                { console.log(formation.uuid)
                var item = this.arr_formation_send.findIndex(pp => pp.uuid == formation.uuid);
                var item_formation = this.arr_formation.findIndex(ite => ite["uuid"] == formation.uuid);
                console.log(item_formation);
                var qte = parseInt(this.arr_formation[item_formation]['place']);
                console.log('qte : ',qte);
                if (qte>0)
                {
                    if( item == -1 )
                        {
                            this.arr_formation_send.push({uuid:formation.uuid,qte:1,nom:formation.titre})
                            this.panier.push({nom:formation.titre,prix:formation.price,qte:1})
                            this.count += 1;
                            this.arr_formation[item_formation]['place']  = (qte - 1).toString();
                        }else{
                            alert('vous avez le droit qu un seul pass');
                        }
                        

                }else{
                    alert('les places non disponibles');
                }

          },
          add_transaction()
             {	
              var url = this.url_base + this.url_transaction;
                
                if(this.products_buy.length >0 )
                    {
                        var prod = {"user":this.uuid,"produit":this.products_buy};
                    }
                if (this.arr_formation_send.length > 0)
                    {
                        var prod = {"user":this.uuid,"formation":this.arr_formation_send};
                    }
                if( this.products_buy.length >0 && this.arr_formation_send.length > 0)
                    {
                        var prod = {"user":this.uuid,"produit":this.products_buy,"formation":this.arr_formation_send};
                    }
                
              axios.post(url,prod,{
                  headers:{
                      "Authorization": "dar " + this.token,
                  }
              })
                .then(response => {
                    console.log(response.data)
                    if( response.status == 200)
                        {
                            tx_hash = response.data.tx_hash
                            console.log("tx_hahs : ", tx_hash);
                            $.toast({
                                heading: 'Well done!',
                                text: ' successfull transaction',
                                position: 'top-right',
                                loaderBg: '#5ba035',
                                icon: 'success',
                                hideAfter: 1500,
                                stack: 1
                            });
                            //clear items
                            this.count = 0;
                            this.products_buy = [];
                            this.panier = [];
                        }
                    if( response.status == 500)
                        {   
                            
                            console.log('failed')
                        }
                })
                .catch(e => {
  
                    console.log(e);
                    alert(e.text);
                 // this.errors.push(e)
                })
             },
          obtaintoken:function()
            {
            this.url_token = this.url_base + this.url_token;
            this.token = sessionStorage.getItem("token");
             if(this.token == null)
                {
                    axios.get(this.url_token)
                    .then(response =>{
                        var  token = response.data.token;
                        this.token = token;
                        sessionStorage.setItem("token", this.token);
                    }
                    )
                }

            },
 

          hide:function(){
              console.log("in fn hide");
              this.salleIsLoaded =false;
              this.prodIsLoaded = true;
          },
          //FINAL TO GET PRODUCT 
          produit:function()
            {
              url_produit = this.url_base + this.url_getProduct
              console.log(url_produit);
              axios.get(url_produit,{
                headers:{
                    "Authorization": "dar " + this.token,
                }
                })
              .then(response => {
                this.product = response.data;
                console.log(this.product);
                this.prodIsLoaded = true;
              })
              .catch(e => {
                  console.log(e);
              })
          },

        get_historique:function(min_range , max_range)
            {     this.arr_historique  = [];
                if(max_range){
                    if( min_range < max_range)
                        {   var iter = max_range;
                            max_range = min_range;
                            min_range = iter;
                        }
                    url = this.url_base + this.url_historique + "min="+min_range+"&max="+max_range+"/";
                }
                else{
                    url = this.url_base + this.url_historique + "min="+0+"&max="+this.search+"/";
                }
                
                console.log(url);
                var vm = this
                axios.get(url,{
                    headers:{
                        "Authorization": "dar " + this.token,
                    }
                    })
                .then(response =>{
                    console.log(response);
                    if (response.status == 200)
                        {   
                            this.arr_historique = response.data;
                            vm.arr_historique = response.data;
                            console.log('historique     =',this.arr_historique);
                        }
                })
                
            },
        
        get_panier_byUUID:function(uuid_panier)
            {
                this.trans_formation = [];
                this.loading_trans_formation = false;
                this.loading_panier = false;
                url = this.url_base + this.url_panier + uuid_panier
                console.log(url);
                axios.get(url,{
                    headers:{
                        "Authorization": "dar " + this.token,
                    }
                    })
                .then(response =>{
                    if (response.status == 200)
                        { 
                            console.log('response formation',response.data.formations.length);
                            if(response.data.formations.length > 0)
                                {
                                    this.trans_formation = response.data.formations;
                                    this.loading_trans_formation = true;
                                }
                            if(response.data.produits.length > 0)
                                {
                                    this.trans_prod = response.data.produits;
                                    this.loading_panier = true;
                                }
                            
                        }
                })
            },
        getCookie:function() {
                var cookieValue = null,
                    name = 'token';
                if (document.cookie && document.cookie !== '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                this.token = cookieValue;
            }
        },

        decode_jwt:function(token)
            {   
                this.getCookie()
                var base64Url = token.split('.')[1];
                var base64 = base64Url.replace('-', '+').replace('_', '/');
                var decoded =  JSON.parse(window.atob(base64));
                var orig_iat = decoded.orig_iat;
                var exp = decoded.exp;

                var current_time = Date.now() / 1000;
                if ( exp <= current_time) {
                    alert("session expire");
                  window.location.replace("http://127.0.0.1:8000/dar/logout");
                    console.log("expired");
                }   
                /*
                if(exp - (Date.now()/1000) < 1800 && (Date.now()/1000) - orig_iat < 628200){
                    console.log("refresh token");
                  } else if (exp -(Date.now()/1000) < 1800){
                    // DO NOTHING, DO NOT REFRESH      
                    console.log("do not refresh")    
                  } else {
                  //  window.location.replace("http://127.0.0.1:8000/dar/logout");
                    console.log("re login");
                  }
                */
            },
        get_formation:function()
            {
                url  = this.url_base + this.url_formation
                axios.get(url,{
                    headers:{
                        "Authorization": "dar " + this.token,
                    }
                    })
                  .then(response => {
                      if(response.status == 200)
                      {
                        this.arr_formation = response.data;
                        this.formIsLoaded = true;
                        console.log('Formation      :',this.arr_formation);
                      }
                      else{
                          console.log('error');
                      }
                
                  })
                  .catch(e => {
                      console.log(e);
                  })
            }  
        },
        mounted(){
            this.uuid = this.$refs.uuid.innerHTML;
            this.uuid_dar = this.$refs.uuiddar.innerHTML;
            this.getCookie();
            if(this.token != null){
                console.log('tokzn exist');
                this.decode_jwt(this.token);
            }else{
                console.log("token exist pas");
                window.location.replace("http://127.0.0.1:8000/dar/logout");
            }

            this.produit();
            this.get_formation();

            
        },
      });

