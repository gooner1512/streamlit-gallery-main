class Html:   

    def html_block_4(label, text_val1, p1, p2):        
        html = """
                <div class="container text-center block-4">
                    <div class="row align-items-center">
                        <div class="col-6 col-sm-6 col-md-12 col-lg-12 col-xl-6">
                            <label>{label}</label>
                            <h2 class="block-4-h2">{text_val1}</h2>
                        </div>
                        <div class="col-6 col-sm-6 col-md-12 col-lg-12 col-xl-6">
                            {p1}
                            {p2}
                        </div>
                    </div>
                </div>"""
        return html.format(label=label, text_val1=text_val1, p1 = p1, p2 = p2)

    def html_block_3(label, text_val1, p1):        
        html = """
                <div class="container text-center block-4">
                    <div class="row align-items-center">
                        <div class="col-6 col-sm-6 col-md-12 col-lg-12 col-xl-6">
                            <label>{label}</label>
                            <h2 class="block-4-h2">{text_val1}</h2>
                        </div>
                        <div class="col-6 col-sm-6 col-md-12 col-lg-12 col-xl-6">
                            {p1}
                        </div>
                    </div>
                </div>"""
        return html.format(label=label, text_val1=text_val1, p1 = p1)
    
