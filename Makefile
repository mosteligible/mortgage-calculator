post-commit:
	git push; \
	docker build -t mosteligible/mortgage-detailer:latest .; \
	docker push mosteligible/mortgage-detailer:latest
