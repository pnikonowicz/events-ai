from fetch.eventbrite.to_json import html_to_json

def test_html_to_json():
    html_text=""" 
<html>
    <div>
        <img src="div_A_img"></img>
        <a href="div_A_href"></a>
        <h3>div_A_title</h3>
        <p>ignored</p>
        <p>day • time</p>
        <p>location</p>
    </div>
        
    <div>
        <a href="div_B_href"></a>
        <h3>div_B_title</h3>
    </div>

    <div>
        <a href="div_C_href"></a>
        <h3>div_C_title</h3>
        <p>ignored</p>
        <p>this does not have a delimeter</p>
    </div>
</html>

"""
    
    result = html_to_json(html_text)

    assert len(result) == 3

    assert result[0]["image"] == "div_A_img"
    assert result[0]["link"] == "div_A_href"
    assert result[0]["title"] == "div_A_title"
    assert result[0]["time"] == "time"
    assert result[0]["location"] == "location"

    assert result[1]["image"] == None
    assert result[1]["link"] == "div_B_href"
    assert result[1]["title"] == "div_B_title"
    assert result[1]["time"] == None
    assert result[1]["location"] == None

    assert result[2]["time"] == None
    assert result[2]["location"] == None