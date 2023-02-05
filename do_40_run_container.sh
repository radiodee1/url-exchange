
sudo -E docker run  -e OPENAI_API_KEY -e GPT_ETC_GPTJ_KEY -e GPT_ETC_GPTJ_MODEL -it url_exchange ./do_10_start_main.sh $@  

clear 

echo "./do_30_run_container.sh"
echo "Use options like '--timer' and '--gptj'"
#sudo -E docker run  -e OPENAI_API_KEY -e GPT_ETC_GPTJ_KEY -e GPT_ETC_GPTJ_MODEL -it url_exchange


#/bin/bash ./do_10_start_main.sh


#docker exec -it url_exchange /bin/bash
