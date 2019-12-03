let Knot = function (name, X, Y, item_pre, item_suc, last_time, earliest_start_time, earliest_finish_time, latest_start_time, latest_finish_time, free_time_difference, total_time_difference, key) {
    this.name = name;
    this.X = X;
    this.Y = Y;
    this.item_pre = item_pre || "无";
    this.item_suc = item_suc || "无";
    this.earliest_start_time = earliest_start_time || "无";
    this.earliest_finish_time = earliest_finish_time || "无";
    this.latest_start_time = latest_start_time || "无";
    this.latest_finish_time = latest_finish_time || "无";
    this.free_time_difference = free_time_difference || "无";
    this.total_time_difference = total_time_difference || "无";
    this.key = key || false;
}

// Knot.prototype = {
// 	//画小星星
// 	drawStar:function( ctx , r , rot , borderWidth , borderStyle , fillStyle){
//            let R = r*2;
//            ctx.beginPath();
//            for( let i = 0 ; i < 5 ; i ++){
//                ctx.lineTo(Math.cos((18+72*i - rot)/180*Math.PI) * R + this.X ,- Math.sin((18+72*i - rot )/180*Math.PI) * R + this.Y);
//                ctx.lineTo(Math.cos((54+72*i - rot)/180*Math.PI) * r + this.X ,- Math.sin((54+72*i - rot )/180*Math.PI) * r + this.Y);
//            }
//            ctx.closePath();

//            ctx.lineWidth = borderWidth||2;
//            ctx.strokeStyle = borderStyle||"#F9F900";
//            ctx.fillStyle = fillStyle||"#FFFF37";
//            ctx.fill();
//            ctx.stroke();
//    	},

// //获取鼠标在canvas画布上的位置(**不是浏览器窗口的鼠标位置)
// getMousePos:function(canvas, event) {
//        let rect = canvas.getBoundingClientRect();

//        let x = event.clientX - rect.left * (canvas.width / rect.width);
//        let y = event.clientY - rect.top * (canvas.height / rect.height);
//        return { x , y }

//    },

//    onClick:function(callBack){
//        // let f = function (evt) {
//            let mousePos = this.getMousePos(this.canvas, event);
//            let mouseX = mousePos.x;
//            let mouseY = mousePos.y;
//            let distance = Math.sqrt((mouseX - this.X) * (mouseX - this.X) + (mouseY - this.Y) * (mouseY - this.Y));
//            alert(distance);
//        // },
//    },

//     if(distance <= 12){
//         alert(this.item_pre)
//     }
// }

// this.canvas.removeEventListener('click',f);
// this.canvas.addEventListener("click", f);

//         },
//     },
// }

// function getMousePos(canvas, event) {
//     //1
//     var rect = canvas.getBoundingClientRect();
//     //2
//     var x = event.clientX - rect.left * (canvas.width / rect.width);
//     var y = event.clientY - rect.top * (canvas.height / rect.height);
//     console.log("x:" + x + ",y:" + y );
// }


    
		
